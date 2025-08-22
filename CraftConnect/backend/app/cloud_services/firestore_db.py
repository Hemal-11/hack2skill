from google.cloud.firestore_v1.async_client import AsyncClient
from app.config.settings import settings

db = AsyncClient(project=settings.PROJECT_ID, database=settings.FIRESTORE_DB)

CACHE_COLLECTION = "copilot_cache"

async def set_cached_analysis(image_hash: str, data: dict):
    """Saves analysis data to Firestore."""
    doc_ref = db.collection(CACHE_COLLECTION).document(image_hash)
    await doc_ref.set(data)

async def get_cached_analysis(image_hash: str) -> dict | None:
    """Retrieves analysis data from Firestore if it exists."""
    doc_ref = db.collection(CACHE_COLLECTION).document(image_hash)
    doc = await doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None