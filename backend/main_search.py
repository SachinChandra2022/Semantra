import os
import json
from embedding_utils import embed_texts
from search_utils import FaissIndex

# Constants
PROCESSED_DATA_PATH = "data/processed"
INDEX_SAVE_PATH = "models/faiss_index"
TOP_K_RESULTS = 5

def load_corpus(directory):
    """
    Load all processed .txt documents from the directory into a list.
    """
    documents = []
    filenames = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    documents.append(content)
                    filenames.append(filename)
    return documents, filenames

def main():
    # Step 1: Load documents
    print("🔍 Loading corpus...")
    documents, filenames = load_corpus(PROCESSED_DATA_PATH)
    if not documents:
        print("❌ No documents found in the processed data folder.")
        return

    # Step 2: Generate embeddings
    print("🧠 Embedding documents...")
    doc_embeddings = embed_texts(documents)

    # Step 3: Build FAISS index
    print("⚙️ Building FAISS index...")
    dim = doc_embeddings.shape[1]
    index = FaissIndex(dim)
    index.add(doc_embeddings, documents)

    # Optional: Save index if your FaissIndex class supports it
    # index.save(INDEX_SAVE_PATH)

    # Step 4: Query loop
    print("✅ Ready for queries! Type 'exit' to stop.")
    while True:
        query = input("\n🔎 Enter your search query: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting search.")
            break

        query_embedding = embed_texts([query])
        results = index.search(query_embedding, top_k=TOP_K_RESULTS)

        print("\n📄 Top Matches:")
        for i, (match, score) in enumerate(results[0]):
            print(f"{i+1}. [Score: {score:.4f}] {match[:200]}{'...' if len(match) > 200 else ''}")

if __name__ == "__main__":
    main()