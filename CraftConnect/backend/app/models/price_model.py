import logging
import math
from app.cloud_services.firestore_db import db
from google.cloud import firestore_v1 as firestore
from app.models.vertex_text import vertex_text_client

logger = logging.getLogger(__name__)

class PriceSuggestionService:
    async def get_pricing_data(self, category: str) -> dict:
        """Fetches all necessary pricing rules and comparable data in one go."""
        rules_doc = await db.collection('pricing_rules').document('default').get()
        rules = rules_doc.to_dict() if rules_doc.exists else {}

        products_ref = db.collection('products').where(filter=firestore.FieldFilter('category', '==', category))
        docs = products_ref.stream()
        prices = [doc.to_dict().get('price', 0) async for doc in docs if doc.exists]
        
        market_avg = sum(prices) / len(prices) if prices else 0.0
        
        return {
            "rules": rules,
            "num_comparables": len(prices),
            "market_avg": market_avg
        }

    def _determine_confidence(self, num_comparables: int) -> str:
        if num_comparables >= 4:
            return "High"
        if num_comparables >= 1:
            return "Medium"
        return "Low"

    async def generate_explanation(self, inputs: dict) -> str:
        """Uses Gemini to generate an empathetic and encouraging explanation."""
        system_prompt = """
        You are a kind and encouraging business advisor for artisans. Your goal is to explain a price suggestion in a simple, positive, and empowering way.
        - Start by acknowledging the artisan's hard work.
        - Justify the price based on the provided costs, labor, and margin.
        - Reference the market data and the confidence level to build trust.
        - End with an encouraging statement that the final decision is theirs.
        - Keep the explanation concise (3-4 sentences) and use Indian Rupees (₹) as the currency symbol.
        """

        confidence_text = {
            "Low": "Since we don't have much market data for this specific category, the upper range is based on general trends. This is a great starting point!",
            "Medium": "This price positions your piece competitively based on a few similar items we've seen.",
            "High": "This price is strongly aligned with the current market, positioning your beautiful work competitively."
        }[inputs['confidence']]

        user_prompt = f"""
        Here is the data for a price suggestion. Please write the explanation.
        - Material Cost: ₹{inputs['materials_cost']:.2f}
        - Labor Hours: {inputs['labor_hours']} hours
        - Calculated Base Price (Cost + Labor + Margin): ₹{inputs['base_price']:.2f}
        - Confidence Level: {inputs['confidence']}
        - Market Context: {confidence_text}
        - Final Suggested Price Range: ₹{inputs['min_price']:.0f} to ₹{inputs['max_price']:.0f}
        """
        
        explanation = await vertex_text_client.generate_content(system_prompt, user_prompt)
        return explanation

    async def suggest_price(self, materials_cost: float, labor_hours: float, category: str) -> dict:
        pricing_data = await self.get_pricing_data(category)
        rules = pricing_data['rules']
        num_comparables = pricing_data['num_comparables']
        
        confidence = self._determine_confidence(num_comparables)

        hourly_rate = rules.get('hourly_rate_inr', 200)
        margin = rules.get('margin_percentage', 15)
        
        cost_plus_labor = materials_cost + (labor_hours * hourly_rate)
        base_price = cost_plus_labor * (1 + margin / 100)

        # De-risked market price calculation
        if num_comparables > 1:
            market_influence_price = pricing_data['market_avg']
        else:
            # Fallback to national average if not enough data
            market_influence_price = rules.get('national_average_price', {}).get(category, base_price * 1.2)

        # Determine Range
        min_price = base_price
        max_price = max(base_price, market_influence_price * 1.1) # Ensure max is always > min
        suggested_price = (min_price + max_price) / 2
        
        # Round prices to a cleaner number
        def round_to_nearest_5(n):
            return 5 * round(n / 5)

        # Generate Explanation
        explanation_inputs = {
            "materials_cost": materials_cost, "labor_hours": labor_hours,
            "base_price": base_price, "confidence": confidence,
            "min_price": min_price, "max_price": max_price,
        }
        explanation = await self.generate_explanation(explanation_inputs)

        return {
            "min_price": round_to_nearest_5(min_price),
            "max_price": round_to_nearest_5(max_price),
            "suggested_price": round_to_nearest_5(suggested_price),
            "explanation": explanation,
            "confidence": confidence,
        }

price_suggestion_service = PriceSuggestionService()