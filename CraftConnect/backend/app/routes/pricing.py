# backend/app/routes/pricing.py

from fastapi import APIRouter, HTTPException, status
from app.schemas.pricing import PriceSuggestionRequest, PriceSuggestionResponse
from app.models.price_model import price_suggestion_service

router = APIRouter()

@router.post(
    "/suggest",
    response_model=PriceSuggestionResponse,
    summary="Suggest a Price for an Artisan's Product",
    tags=["Pricing"]
)
async def suggest_product_price(request: PriceSuggestionRequest):
    try:
        suggestion = await price_suggestion_service.suggest_price(
            materials_cost=request.materials_cost,
            labor_hours=request.labor_hours,
            category=request.category
        )
        return suggestion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}"
        )