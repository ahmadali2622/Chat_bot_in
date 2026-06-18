# NetSol Chatbot — FastAPI + LangGraph + Gemini 2.5 Flash-Lite + RAG (ChromaDB) + React

## 📁 Project Structure
```
chatbot-project/
├── README.md
├── backend/
│   ├── main.py             # FastAPI app & routes
│   ├── graph.py             # LangGraph state, nodes, graph definition
│   ├── models.py            # Pydantic request/response models
│   ├── config.py            # CORS & app settings
│   ├── scraper.py           # Scrapes NetSol Technologies website
│   ├── scraped_data.txt     # Raw scraped text (scraper.py output)
│   ├── build_index.py       # Chunks + embeds scraped_data.txt -> ChromaDB
│   ├── chroma_db/           # Persisted ChromaDB vector store (build_index.py output)
│   ├── requirements.txt
│   └── .env.example         # template for your API key
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── App.css
        └── components/
            ├── ChatWindow.jsx
            ├── Message.jsx
            └── ChatInput.jsx
```

---

## ⚙️ Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Add your Gemini API key:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and paste your key:
     ```
     GEMINI_API_KEY=your_actual_key_here
     ```
   - Get a free key at: https://aistudio.google.com/app/apikey
5. **Build the knowledge base** (one-time, or whenever site content changes — see [RAG Pipeline](#-rag-pipeline-how-it-works) below):
   ```bash
   python scraper.py
   python build_index.py
   ```
6. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
7. Verify it's running by visiting:
   ```
   http://127.0.0.1:8000
   ```
   → `{"status": "Chatbot API is running"}`

---

## 🌐 Frontend Setup (React + Vite)

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```
4. Open the URL shown (usually `http://localhost:5173`)

> Make sure the backend is running on `http://127.0.0.1:8000` — the React app's `API_URL` in `src/App.jsx` points there by default.

---

## 🧠 How It Works

### Chat flow (LangGraph)
```
START → retrieve_node → chatbot_node → END
```

1. **`retrieve_node`** takes the user's message, embeds it, and queries ChromaDB for the most relevant chunks of NetSol website content.
2. **`chatbot_node`** takes the original user message plus the retrieved chunks, builds a grounded prompt, and sends it to **Gemini 2.5 Flash-Lite** via the `google-genai` SDK.
3. The model's reply (now grounded in real NetSol content instead of relying purely on its own knowledge) is returned to the frontend.

### RAG pipeline (how the knowledge base is built)

This is the offline pipeline that prepares the data `retrieve_node` searches over. It only needs to be re-run when the source website content changes.

```
scraper.py  →  scraped_data.txt  →  build_index.py  →  chroma_db/
```

| Step | Script | What it does |
|---|---|---|
| 1. Scrape | `scraper.py` | Uses `requests` + `BeautifulSoup` to crawl the NetSol Technologies website and pull out the visible page text. |
| 2. Save raw text | `scraped_data.txt` | The cleaned text output from step 1, saved to disk as a single text file — this is the raw corpus before chunking. |
| 3. Chunk + embed + store | `build_index.py` | Reads `scraped_data.txt`, splits it into smaller overlapping chunks, generates vector embeddings for each chunk using **`sentence-transformers`** (local embedding model, no API call needed), and writes the chunks + embeddings into a persisted **ChromaDB** collection on disk (`chroma_db/`). |
| 4. Retrieve | `retrieve_node` (in `graph.py`) | At request time, embeds the incoming user query with the same `sentence-transformers` model, performs a similarity search against the ChromaDB collection, and returns the top-matching chunks as context. |
| 5. Generate | `chatbot_node` (in `graph.py`) | Combines the user's question with the retrieved context chunks into a single prompt and sends it to Gemini 2.5 Flash-Lite for the final grounded answer. |

**Why this matters:** without retrieval, Gemini only knows what it learned during its own training and can't answer questions about NetSol-specific details. With the scrape → chunk → embed → store → retrieve pipeline above, every answer is grounded in actual scraped content from the NetSol site, which reduces hallucination and keeps answers current with whatever was scraped.

**Re-running the pipeline:** if NetSol's website content changes, just re-run `python scraper.py` followed by `python build_index.py` to refresh `scraped_data.txt` and rebuild the ChromaDB index. The existing `chroma_db/` folder will be overwritten with the new embeddings.

### File responsibilities

| File | Purpose |
|---|---|
| `config.py` | Loads `.env`, holds API key, model name, CORS settings |
| `models.py` | Pydantic schemas for `/chat` request & response |
| `scraper.py` | Scrapes NetSol website text into `scraped_data.txt` |
| `build_index.py` | Chunks + embeds `scraped_data.txt` and stores vectors in ChromaDB |
| `graph.py` | LangGraph state + `retrieve_node` (ChromaDB search) + `chatbot_node` (Gemini call) |
| `main.py` | FastAPI app, CORS middleware, `/chat` endpoint |

---

## 🔑 Where to Put Your Gemini API Key

Put it **only** in the `.env` file inside `backend/`:
```
GEMINI_API_KEY=your_actual_key_here
```
- `.env` should be in `.gitignore` (never commit your key to the repo).
- `config.py` reads it via `os.getenv("GEMINI_API_KEY")`.

---

## 🔧 Possible Next Steps

- Add source citations to chatbot replies (show which scraped page/section a chunk came from)
- Add a scheduled job to re-run `scraper.py` + `build_index.py` periodically so the index stays fresh automatically
- Swap `sentence-transformers` for a hosted embedding API if you outgrow local embeddings
- Add chat history / multi-turn memory to the LangGraph state
- Deploy backend + frontend (e.g. Render/Railway for FastAPI, Vercel/Netlify for the React app)
