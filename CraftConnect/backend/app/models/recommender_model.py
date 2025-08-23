from typing import List
import logging
from datetime import datetime, timedelta, timezone
import numpy as np
from app.cloud_services.firestore_db import db
from app.cloud_services.faiss_service import faiss_index
from app.models.vertex_text import vertex_text_client

logger = logging.getLogger(__name__)

class RecommenderService:
    async def get_recommendations(self, product_id: str, fairness_boost: bool = False) -> List[dict]:
        print("\n--- STARTING RECOMMENDATION TRACE ---")

        # 1. Fetch the target product's data and embedding
        product_ref = db.collection('products').document(product_id)
        product_doc = await product_ref.get()
        print(f"DEBUG 1: Fetched product doc for '{product_id}'. Exists: {product_doc.exists}")
        if not product_doc.exists:
            print("--- ENDING TRACE: Product not found ---")
            return []
        
        product_data = product_doc.to_dict()
        query_embedding = product_data.get('description_embedding')
        print(f"DEBUG 2: Found embedding for product? {'Yes' if query_embedding else 'No'}")
        if not query_embedding:
            print("--- ENDING TRACE: Embedding not found in document ---")
            return []

        # 2. Find N nearest neighbors in FAISS
        candidate_ids = faiss_index.search(np.array(query_embedding), k=5)
        print(f"DEBUG 3: FAISS search returned IDs: {candidate_ids}")
        
        # Filter out the original product_id from the results
        candidate_ids = [pid for pid in candidate_ids if pid != product_id]
        print(f"DEBUG 4: Candidate IDs after filtering self: {candidate_ids}")
        if not candidate_ids:
            print("--- ENDING TRACE: No other similar products found ---")
            return []

        # 3. Fetch candidate product details from Firestore
        candidate_docs = await db.collection('products').where('__name__', 'in', candidate_ids).get()
        candidates = [{'id': doc.id, **doc.to_dict()} for doc in candidate_docs]
        print(f"DEBUG 5: Fetched {len(candidates)} candidate details from Firestore.")

        # ... (the rest of the function for fairness and explanations remains the same) ...
        # ... it will just return empty if len(candidates) is 0 ...
        print("--- ENDING TRACE: Preparing final recommendations ---")
        
        # For this test, we will just return the raw candidates to see if we get this far
        final_recommendations = []
        for rec_product in candidates[:5]:
            final_recommendations.append({
                "id": rec_product['id'],
                "name": rec_product.get('name', 'N/A'),
                "image_url": rec_product.get('image_url', ''),
                "explanation": "Test explanation" # Bypassing Gemini call for this test
            })
            
        return final_recommendations


recommender_service = RecommenderService()