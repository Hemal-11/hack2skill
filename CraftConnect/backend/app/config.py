# backend/app/config.py

import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the path to the root of our backend project to find the .env file
BACKEND_DIR = pathlib.Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    """
    Holds all configuration for the application, loaded from the .env file.
    The app will not start if any of these are missing.
    """
    # Required settings loaded from .env file
    PROJECT_ID: str
    FIRESTORE_DB: str
    BUCKET_NAME: str

    # Settings with default values
    GEMINI_MODEL_ID: str = "gemini-1.5-flash-001"
    EMBEDDING_MODEL_ID: str = "text-embedding-004"
    TRANSLATION_QA_THRESHOLD: float = 0.85
    EMBEDDING_REGION: str = "us-central1"

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        extra='ignore'
    )

# Create a single, globally accessible instance of the settings
settings = Settings()