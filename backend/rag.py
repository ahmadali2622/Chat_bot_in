"""
rag.py
------
Handles the "Retrieval" part of RAG (Retrieval-Augmented Generation).

What it does (step by step):
1. Load the same HuggingFace embedding model used in build_index.py.
2. Connect to the existing ChromaDB database on disk.
3. Given a user question, turn it into an embedding too.
4. Ask ChromaDB for the most similar chunks (closest meaning).
5. Return those chunks as plain text, ready to paste into the
   Gemini prompt.
"""

from langchain_huggingface import HuggingFaceEmbeddings
import chromadb

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "netsol_knowledge"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 3  # how many chunks to retrieve per question

# ---------------------------
# Load model + DB connection once, when this file is imported.
# (Loading the model on every request would be slow.)
# ---------------------------
print("Loading embedding model for retrieval...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

try:
    collection = chroma_client.get_collection(COLLECTION_NAME)
except Exception:
    collection = None
    print(
        f"⚠️ Could not find ChromaDB collection '{COLLECTION_NAME}'. "
        f"Did you run build_index.py first?"
    )


def retrieve_context(query: str, top_k: int = TOP_K) -> str:
    """
    Given a user question, returns the most relevant chunks of
    scraped website text, joined together as one string.

    If the database isn't ready yet, returns an empty string so the
    chatbot can still respond (just without extra context).
    """
    if collection is None:
        return ""

    query_embedding = embedding_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    # results["documents"] looks like: [["chunk1", "chunk2", "chunk3"]]
    matched_chunks = results["documents"][0] if results["documents"] else []

    context = "\n\n---\n\n".join(matched_chunks)
    return context
