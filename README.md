# NetSol Chatbot — FastAPI + LangGraph + Gemini 2.5 Flash-Lite + React
## 📁 Project Structure
```
chatbot-project/
├── README.md
├── backend/
│   ├── main.py          # FastAPI app & routes
│   ├── graph.py          # LangGraph state, nodes, graph definition
│   ├── models.py         # Pydantic request/response models
│   ├── config.py         # CORS & app settings
│   ├── requirements.txt
│   └── .env.example       # template for your API key
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
5. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
6. Verify it's running by visiting:
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
**LangGraph flow:**
```
START → chatbot_node → END
```
`chatbot_node` (in `graph.py`) sends the user's message to **Gemini 2.5 Flash-Lite** via the `google-genai` SDK and returns the model's reply.
**File responsibilities:**
| File | Purpose |
|---|---|
| `config.py` | Loads `.env`, holds API key, model name, CORS settings |
| `models.py` | Pydantic schemas for `/chat` request & response |
| `graph.py` | LangGraph state + Gemini-powered node |
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
## 🔧 Next Steps (RAG Pipeline)
1. Scrape NetSol Technologies website content (`requests` + `BeautifulSoup`)
2. Chunk and embed the text (e.g. `sentence-transformers`)
3. Store embeddings in a vector DB (FAISS / ChromaDB)
4. Add a `retrieve_node` to `graph.py` before `chatbot_node`:
   ```
   START → retrieve_node → chatbot_node → END
   ```
5. Pass retrieved context into the Gemini prompt for grounded (RAG) answers
