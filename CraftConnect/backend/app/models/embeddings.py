import logging
import numpy as np
from typing import List
import vertexai
from vertexai.language_models import TextEmbeddingModel
from app.config.settings import settings

logger = logging.getLogger(__name__)

class VertexEmbeddings:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL_ID):
        # ✅ Initialize Vertex AI in embeddings region only
        vertexai.init(project=settings.PROJECT_ID, location=settings.EMBEDDING_REGION)
        self.model = TextEmbeddingModel.from_pretrained(model_name)
        logger.info(f"Initialized Vertex AI Embedding model: {model_name}")

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate embeddings for input text.
        """
        # ✅ New API expects dict input with content + task_type
        embeddings = self.model.get_embeddings([text])
        return embeddings[0].values

    def get_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.
        """
        dot = np.dot(vec1, vec2)
        norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
        return float(dot / (norm1 * norm2)) if norm1 and norm2 else 0.0


# ✅ Singleton client (so we don’t re-init every time)
embedding_client = VertexEmbeddings()
