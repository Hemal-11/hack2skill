import faiss
import pickle

try:
    index = faiss.read_index("index.faiss")
    with open("mapping.pkl", "rb") as f:
        mapping = pickle.load(f)

    print("✅ Index Test SUCCESSFUL!")
    print(f"   - Number of vectors in index: {index.ntotal}")
    print(f"   - Number of IDs in mapping: {len(mapping)}")

except Exception as e:
    print(f"❌ Index Test FAILED: {e}")