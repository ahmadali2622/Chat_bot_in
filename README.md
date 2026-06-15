# NetSol Chatbot — Day 1 (Frontend + Backend Integration)

A simple chatbot demonstrating FastAPI + LangGraph backend integrated with
a vanilla JS/HTML/CSS frontend.

## Project Structure

```
netsol-chatbot/
├── backend/
│   ├── main.py           # FastAPI app + LangGraph chatbot logic
│   └── requirements.txt
└── frontend/
    └── index.html        # Chat UI (HTML/CSS/JS)
```

## How It Works

1. **Frontend** (`index.html`) — chat bubble UI. User types a message,
   JS sends a POST request to the backend `/chat` endpoint.

2. **Backend** (`main.py`) — FastAPI server exposes `/chat`. The request
   flows through a **LangGraph** graph with two nodes:
   - `process_input` — cleans/normalizes the user's text
   - `generate_response` — generates a reply (currently rule-based;
     replace with an LLM call or RAG retrieval on Day 2)

3. The response is sent back as JSON and displayed in the chat UI.

## Setup & Run

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend will run at: http://127.0.0.1:8000
Test it: http://127.0.0.1:8000/docs (Swagger UI)

### 2. Frontend

Just open `frontend/index.html` in a browser
(or serve it with `python -m http.server` from the `frontend/` folder).

Make sure the backend is running first — the frontend calls
`http://127.0.0.1:8000/chat`.

## Next Steps (Day 2)

- Scrape NetSol Technologies website content (requests + BeautifulSoup)
- Chunk and embed the content (sentence-transformers)
- Store embeddings in a vector DB (ChromaDB / FAISS)
- Add a `retrieve_context` node in the LangGraph before `generate_response`
  to build a RAG pipeline — the bot will then answer using real
  scraped NetSol content instead of placeholder logic
