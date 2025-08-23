from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    """ Defines the input for a translation request. """
    text: str = Field(..., description="The source text to be translated.")
    target_language_code: str = Field(..., description="The ISO 639-1 code for the target language.", examples=["hi"])
    artisan_id: Optional[str] = Field(None, description="Optional ID of the artisan to use their custom glossary.")

class TranslationResponse(BaseModel):
    """ Defines the output of a translation with its quality score. """
    translated_text: str
    quality_score: float
    is_quality_ok: bool