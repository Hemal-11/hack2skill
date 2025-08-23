# backend/app/routes/storyteller.py

from fastapi import APIRouter, HTTPException, status, Body
import logging

from app.models.vertex_text import vertex_text_client
from app.schemas.story import StoryRequest, StoryResponse


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/generate",
    response_model=StoryResponse,
    summary="Generate a Polished Product Story",
    description="Takes an artisan's heritage and a piece-specific story and uses Gemini to generate a cohesive narrative.",
    tags=["Storyteller"]
)
async def generate_story(
    request: StoryRequest = Body(...)
) -> StoryResponse:
    """
    Generates a product story by combining two prompts using the Vertex AI Gemini model.

    - **artisan_heritage**: Text about the artisan's background.
    - **piece_story**: Text about the specific artwork.
    \f
    :param request: The StoryRequest model containing the two prompts.
    :return: A StoryResponse model with the generated narrative.
    """
    if not request.artisan_heritage or not request.piece_story:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both artisan_heritage and piece_story fields are required."
        )

    try:
        polished_story = await vertex_text_client.generate_story_from_prompts(
            artisan_heritage=request.artisan_heritage,
            piece_story=request.piece_story
        )
        return StoryResponse(generated_story=polished_story)
        
    except Exception as e:
        logger.error(f"Failed to generate story: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The story generation service is currently unavailable. Please try again later."
        )