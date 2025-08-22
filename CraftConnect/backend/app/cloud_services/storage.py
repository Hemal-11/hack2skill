from google.cloud import storage as gcs
from app.config.settings import settings
import asyncio

storage_client = gcs.Client(project=settings.PROJECT_ID)

async def upload_file_async(file_content: bytes, destination_blob_name: str) -> str:
    """Uploads a file to the bucket and returns its GCS URI."""
    try:
        bucket = storage_client.bucket(settings.BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)

        # Run blocking upload in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            blob.upload_from_string,
            file_content,
            'image/jpeg'
        )

        return f"gs://{settings.BUCKET_NAME}/{destination_blob_name}"
    except Exception as e:
        print(f"Error uploading to GCS: {e}")
        return None