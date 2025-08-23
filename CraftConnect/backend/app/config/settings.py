import os
import pathlib
from typing import Optional
     
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    GEMINI_MODEL: str
    GEMINI_MODEL_ID: str = "gemini-1.5-flash"
    EMBEDDING_MODEL_ID: str = "text-embedding-004"
    TRANSLATION_QA_THRESHOLD: float = 0.85
    EMBEDDING_REGION: str = "us-central1"
    REGION: str
    FIRESTORE_DB: str
    BUCKET_NAME: str
    FIRESTORE_EMULATOR_HOST: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()

# Set the environment variable for Google credentials
if settings.GOOGLE_APPLICATION_CREDENTIALS:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS