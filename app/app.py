import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from backend.embedding_utils import embed_texts
from backend.search_utils import FaissIndex
import pickle

# ---- Paths ----
index_path = "embedding/faiss_index.bin"
docs_path = "embedding/docs.pkl"
documents_dir = "data/"  # adjust this to wherever your raw docs are stored

# ---- Auto Indexing Function ----
def build_faiss_index():
    st.warning("FAISS index or document store not found. Building now...")

    from backend.preprocess import load_and_split_documents  # Your custom loader
    from backend.embedding_utils import embed_texts

    docs = load_and_split_documents(documents_dir)
    embeddings = embed_texts([doc['content'] for doc in docs])  # Assuming dicts with 'content'

    dim = embeddings.shape[1]
    faiss_index = FaissIndex(dim)
    faiss_index.add(embeddings, [doc['content'] for doc in docs])

    # Save
    faiss_index.save(index_path)
    with open(docs_path, "wb") as f:
        pickle.dump([doc['content'] for doc in docs], f)

    st.success("Indexing complete.")

# ---- Load FAISS index and document store ----
@st.cache_resource
def load_index():
    if not os.path.exists(index_path) or not os.path.exists(docs_path):
        build_faiss_index()

    with open(docs_path, "rb") as f:
        docs = pickle.load(f)

    dim = 384  # For SentenceTransformer 'all-MiniLM-L6-v2'
    faiss_index = FaissIndex(dim)
    faiss_index.load(index_path)
    faiss_index.documents = docs
    return faiss_index

index = load_index()

# ---- Streamlit UI ----
st.set_page_config(page_title="SmartSearch", layout="wide")
st.title("🔍 SmartSearch: Semantic Document Search")
st.markdown("Enter a natural language query below to find relevant information from the processed documents.")

# Input area
query = st.text_input("Enter your search query:", "What is machine learning?", key="query_input")

# Results area
if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Embedding query and retrieving results..."):
            query_emb = embed_texts([query])
            results = index.search(query_emb, top_k=5)

        st.subheader("🔎 Top Results:")
        for i, (hit, score) in enumerate(results[0]):
            with st.expander(f"Result {i+1} — Score: {score:.4f}"):
                st.write(hit)

        st.success("Search complete.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using FAISS, SentenceTransformers, and Streamlit")