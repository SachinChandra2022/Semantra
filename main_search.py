from embedding_utils import embed_texts
from search_utils import FaissIndex

# Sample corpus
documents = [
    "Machine learning is a method of data analysis.",
    "Artificial intelligence includes machine learning.",
    "Deep learning is a subset of machine learning.",
    "Natural language processing deals with text data."
]

# Step 1: Embed all documents
embeddings = embed_texts(documents)

# Step 2: Build FAISS index
dim = embeddings.shape[1]
index = FaissIndex(dim)
index.add(embeddings, documents)

# Step 3: Embed a query and search
query = ["What is machine learning?"]
query_emb = embed_texts(query)
results = index.search(query_emb, top_k=3)

print("Search results:")
for hit, score in results[0]:
    print(f"Score: {score:.4f} - Text: {hit}")