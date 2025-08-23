# backend/app/routes/recommender.py

from fastapi import APIRouter, HTTPException, status
from app.schemas.recommender import RecommendationResponse, RecommendedProduct
from app.models.recommender_model import recommender_service

router = APIRouter()

@router.get(
    "/products/{product_id}/similar",
    response_model=RecommendationResponse,
    summary="Get Similar Products with optional Fairness Boost",
    tags=["Recommendations"]
)
async def get_similar_products(product_id: str, fairness: bool = False):
    try:
        recommendations_data = await recommender_service.get_recommendations(
            product_id=product_id, 
            fairness_boost=fairness
        )
        
        products = [RecommendedProduct(**data) for data in recommendations_data]
        return RecommendationResponse(products=products)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred: {e}"
        )