import logging
import re
from google.cloud import translate_v3 as translate
from app.config.settings import settings
from app.cloud_services.firestore_db import get_artisan_glossary
from app.models.embeddings import embedding_client  # ✅ singleton instance

logger = logging.getLogger(__name__)


class TranslationService:
    def __init__(self):
        self.translate_client = translate.TranslationServiceClient()
        self.parent = f"projects/{settings.PROJECT_ID}/locations/{settings.EMBEDDING_REGION}"
        self.embedding_client = embedding_client  # ✅ use singleton directly

    def _apply_glossary(self, text: str, glossary: dict) -> str:
        """Apply custom artisan glossary before translation."""
        if not glossary:
            return text

        logger.info("Applying custom artisan glossary...")
        for term, translation in glossary.items():
            text = re.sub(rf"\b{re.escape(term)}\b", translation, text, flags=re.IGNORECASE)
        return text

    def _translate(self, text: str, target_language: str, source_language: str = "en") -> str:
        """Perform translation using Google Cloud Translation v3."""
        response = self.translate_client.translate_text(
            request={
                "parent": self.parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )
        return response.translations[0].translated_text

    async def translate_with_qa(self, text: str, target_language_code: str, artisan_id: str = None) -> dict:
        glossary = await get_artisan_glossary(artisan_id, target_language_code) if artisan_id else {}
        text_with_glossary = self._apply_glossary(text, glossary)

        translated_text = self._translate(text_with_glossary, target_language_code)
        back_translated_text = self._translate(translated_text, "en", target_language_code)

        # ✅ use embedding client correctly
        original_embedding = await self.embedding_client.get_embedding(text)
        back_translated_embedding = await self.embedding_client.get_embedding(back_translated_text)

        quality_score = self.embedding_client.get_cosine_similarity(
            original_embedding, back_translated_embedding
        )
        logger.info(f"Translation QA Score: {quality_score:.4f}")

        return {
            "translated_text": translated_text,
            "quality_score": quality_score,
        }


# ✅ Singleton instance
translation_service_client = TranslationService()
