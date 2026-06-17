"""
main.py
-------
FastAPI application entry point.

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_ORIGINS
from models import ChatRequest, ChatResponse
from graph import chat_graph


app = FastAPI(title="LangGraph + Gemini 2.5 Flash-Lite Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Chatbot API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Each request starts from a clean state — no past messages are
    # carried over, so previous chats are never stored or replayed.
    result = chat_graph.invoke(
        {"user_message": request.message, "context": "", "bot_response": ""}
    )
    return ChatResponse(reply=result["bot_response"])
