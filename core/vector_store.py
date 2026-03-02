import faiss
import numpy as np
import os
import pickle

class VectorStore:
    """Manages local storage and retrieval of resume embeddings."""
    
    def __init__(self, dimension: int = 384, index_path: str = "data/vector_db/index.faiss"):
        self.index_path = index_path
        self.dimension = dimension
        
        # Load existing index or create new one
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(index_path + ".meta", "rb") as f:
                self.metadata = pickle.load(f)
        else:
            # L2 distance index for similarity search
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = {} # Map ID -> Resume Name/Text
            os.makedirs(os.path.dirname(index_path), exist_ok=True)

    def add_resume(self, resume_id: str, embedding, text: str):
        # FAISS expects float32 numpy arrays
        vector = np.array([embedding.cpu().numpy()]).astype('float32')
        self.index.add(vector)
        
        # Store metadata
        self.metadata[self.index.ntotal - 1] = {"id": resume_id, "text": text}
        self.save()

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta", "wb") as f:
            pickle.dump(self.metadata, f)