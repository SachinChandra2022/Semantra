import faiss
import numpy as np

class FaissIndex:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query_embedding, top_k=5):
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for scores, idxs in zip(D, I):
            hits = [(self.texts[i], float(score)) for i, score in zip(idxs, scores)]
            results.append(hits)
        return results