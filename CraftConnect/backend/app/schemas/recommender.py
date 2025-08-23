# backend/app/schemas/recommender.py

from pydantic import BaseModel, Field
from typing import List

class RecommendedProduct(BaseModel):
    id: str
    name: str
    image_url: str
    explanation: str = Field(..., description="AI-generated reason for the recommendation.")

class RecommendationResponse(BaseModel):
    products: List[RecommendedProduct]