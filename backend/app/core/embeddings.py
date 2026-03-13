from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str) -> np.ndarray:
    """
    Converts text into embedding vector.
    """
    embedding = model.encode(text)
    return np.array(embedding, dtype="float32")