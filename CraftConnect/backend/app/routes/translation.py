from fastapi import APIRouter, HTTPException, status, Body
import logging

from app.schemas.translation import TranslationRequest, TranslationResponse
from app.models.translation_model import translation_service_client
from app.config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Translate Text with QA and Artisan Glossary",
    tags=["Translation"]
)
async def translate_text_with_qa(request: TranslationRequest = Body(...)):
    try:
        result = await translation_service_client.translate_with_qa(
            text=request.text,
            target_language_code=request.target_language_code,
            artisan_id=request.artisan_id,
        )

        is_quality_ok = result["quality_score"] >= settings.TRANSLATION_QA_THRESHOLD

        return TranslationResponse(
            translated_text=result["translated_text"],
            quality_score=result["quality_score"],
            is_quality_ok=is_quality_ok,
        )
    except Exception as e:
        logger.error(f"Failed during translation QA: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Translation service is currently unavailable."
        )