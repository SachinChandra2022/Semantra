import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from backend.embedding_utils import embed_texts
from backend.search_utils import FaissIndex
import os
import pickle

# ---- Load FAISS index and document store ----
@st.cache_resource
def load_index():
    index_path = "embedding/faiss_index.bin"
    docs_path = "embedding/docs.pkl"

    if not os.path.exists(index_path) or not os.path.exists(docs_path):
        st.error("FAISS index or document store not found. Please run indexing first.")
        st.stop()

    with open(docs_path, "rb") as f:
        docs = pickle.load(f)

    dim = 384  # Assuming SentenceTransformer 'all-MiniLM-L6-v2'
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