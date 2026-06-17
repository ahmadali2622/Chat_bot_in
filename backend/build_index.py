"""
build_index.py
---------------
Builds the RAG knowledge base from the scraped website text.

What it does (step by step):
1. Read scraped_data.txt (created by scraper.py).
2. Split the long text into small chunks using LangChain's
   RecursiveCharacterTextSplitter (it tries to split on paragraph/line
   breaks first, so chunks don't cut sentences in awkward places).
3. Convert each chunk into an embedding (a list of numbers that
   represents its meaning) using a free HuggingFace model.
4. Save all chunks + embeddings into ChromaDB, a simple local vector
   database, stored on disk in the chroma_db/ folder.

Run it once (and again whenever scraped_data.txt changes):
    python build_index.py
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb

INPUT_FILE = "scraped_data.txt"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "netsol_knowledge"

# Free HuggingFace embedding model — small and fast, good for learning/demo use.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 50     # overlap so we don't lose context at chunk boundaries


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text: str) -> list[str]:
    """
    Splits text into overlapping chunks using LangChain's text splitter.
    It tries to split on "\n\n", then "\n", then " " — in that order —
    so chunks stay close to natural paragraph/sentence boundaries
    instead of cutting words in half at a fixed character count.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_text(text)


def main():
    print("Loading scraped text...")
    text = load_text(INPUT_FILE)

    print("Splitting into chunks...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks.")

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME} ...")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    print("Creating embeddings for all chunks...")
    embeddings = embedding_model.embed_documents(chunks)

    print("Saving to ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete old collection if it exists, so we always rebuild fresh
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
    )

    print(f"\nDone! Stored {len(chunks)} chunks in ChromaDB at '{CHROMA_PATH}'")


if __name__ == "__main__":
    main()
