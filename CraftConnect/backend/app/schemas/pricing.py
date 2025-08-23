from pydantic import BaseModel, Field

class PriceSuggestionRequest(BaseModel):
    materials_cost: float = Field(..., gt=0, description="Cost of raw materials in INR.")
    labor_hours: float = Field(..., gt=0, description="Total hours of labor.")
    category: str = Field(..., description="Product category for finding comparables.", examples=["pottery", "textiles"])

class PriceSuggestionResponse(BaseModel):
    min_price: float
    max_price: float
    suggested_price: float
    explanation: str = Field(..., description="AI-generated explanation for the price range.")
    confidence: str = Field(..., description="The confidence level of the suggestion (Low, Medium, High).")