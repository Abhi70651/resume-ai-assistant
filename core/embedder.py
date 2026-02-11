from sentence_transformers import SentenceTransformer, util
import torch

class Embedder:
    """The 'Brain' of the project: Handles vectorization and similarity logic."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load the model once to avoid overhead
        self.model = SentenceTransformer(model_name)
        # Use GPU if available, else CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def get_embedding(self, text: str):
        """Converts text into a high-dimensional vector."""
        return self.model.encode(text, convert_to_tensor=True)

    def compute_similarity(self, embedding_a, embedding_b) -> float:
        """
        Computes Cosine Similarity between two vectors.
        Output is between 0 (completely different) and 1 (identical).
        """
        score = util.cos_sim(embedding_a, embedding_b)
        return float(score.item())
    def get_chunked_embedding(self, text: str, chunk_size: int = 500, overlap: int = 50):
        """
        Splits long resumes into overlapping chunks to stay within token limits.
        Returns a single 'mean' vector representing the entire document.
        """
        words = text.split()
        chunks = [
            " ".join(words[i : i + chunk_size]) 
            for i in range(0, len(words), chunk_size - overlap)
        ]
        
        # Get embeddings for all chunks
        chunk_embeddings = self.model.encode(chunks, convert_to_tensor=True)
        
        # Mean Pooling: Average all chunk vectors into one "Document Vector"
        return torch.mean(chunk_embeddings, dim=0)