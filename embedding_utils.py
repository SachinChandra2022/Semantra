from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts):
    """
    Input: List of strings (texts)
    Output: numpy array of embeddings (float32)
    """
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings
