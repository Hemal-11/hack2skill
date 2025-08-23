import asyncio
import faiss
import numpy as np
import pickle
import logging

# This setup allows the script to import from our 'app' module
import sys
import os
sys.path.append(os.getcwd())

from app.config.settings import settings
from app.models.embeddings import embedding_client
from app.cloud_services.firestore_db import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """
    Fetches all products, generates embeddings, saves them to Firestore,
    and creates a FAISS index for local similarity search.
    """
    logger.info("Starting product indexing...")
    products_ref = db.collection('products')
    all_products = [doc async for doc in products_ref.stream()]

    if not all_products:
        logger.warning("No products found in Firestore. Exiting.")
        return

    product_ids = [p.id for p in all_products]
    # Use description, fall back to name, then empty string
    descriptions = [
        p.to_dict().get('description') or p.to_dict().get('name', '') 
        for p in all_products
    ]
    
    logger.info(f"Found {len(descriptions)} products. Generating embeddings...")
    embeddings = []
    for desc in descriptions:
        embedding = await embedding_client.get_embedding(desc)
        embeddings.append(embedding)
    
    # Save embeddings back to Firestore for individual lookups
    batch = db.batch()
    for i, product_id in enumerate(product_ids):
        product_ref = db.collection('products').document(product_id)
        batch.update(product_ref, {"description_embedding": embeddings[i]})
    await batch.commit()
    logger.info("Embeddings saved back to Firestore documents.")

    # Create and save FAISS index
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    embedding_matrix = np.array(embeddings).astype('float32')
    index.add(embedding_matrix)
    
    # Save the index and the mapping from index position to product_id
    faiss.write_index(index, "index.faiss")
    with open("mapping.pkl", "wb") as f:
        pickle.dump(product_ids, f)
    
    logger.info("FAISS index (index.faiss) and mapping file (mapping.pkl) created successfully.")
    logger.info("Indexing complete!")


if __name__ == "__main__":
    import vertexai
    # Initialize Vertex AI SDK specifically for this script
    vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
    
    asyncio.run(main())