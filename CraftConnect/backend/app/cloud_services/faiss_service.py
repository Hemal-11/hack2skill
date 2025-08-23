import faiss
import numpy as np
import pickle
from typing import List
import logging
import os

logger = logging.getLogger(__name__)

class FaissIndex:
    def __init__(self, index_path="index.faiss", mapping_path="mapping.pkl"):
        self.index = None
        self.product_id_map = []
        # Load the index immediately upon creation
        self._load_index(index_path, mapping_path)

    def _load_index(self, index_path: str, mapping_path: str):
        try:
            # Check if files exist before trying to load
            if not os.path.exists(index_path) or not os.path.exists(mapping_path):
                raise FileNotFoundError(f"Index files not found. Ensure '{index_path}' and '{mapping_path}' exist.")

            self.index = faiss.read_index(index_path)
            with open(mapping_path, "rb") as f:
                self.product_id_map = pickle.load(f)
            
            if self.index.ntotal == 0:
                raise ValueError("FAISS index is empty. Please re-run the indexing script.")
            
            logger.info(f"✅ FAISS index loaded successfully. {self.index.ntotal} vectors indexed.")

        except (FileNotFoundError, ValueError) as e:
            logger.error(f"❌ Critical error loading FAISS index: {e}")
            # In a real app, you might want to handle this more gracefully,
            # but for the hackathon, crashing on startup is better than failing silently.
            raise e

    def search(self, query_embedding: np.ndarray, k: int) -> List[str]:
        if not self.index:
            logger.warning("Search called but FAISS index is not available.")
            return []
        
        # --- Debug Prints to be sure ---
        print(f"DEBUG: Index has {self.index.ntotal} vectors.")
        print(f"DEBUG: Query embedding shape: {query_embedding.shape}")
        # --------------------------------

        distances, indices = self.index.search(query_embedding.astype('float32').reshape(1, -1), k)
        return [self.product_id_map[i] for i in indices[0] if i < len(self.product_id_map)]

# This line now creates the instance AND loads the index immediately.
faiss_index = FaissIndex()