"""
FastAPI + LangGraph Chatbot Backend
-------------------------------------
Day 1 Task: Simple chatbot with frontend-backend integration.

Run with:
    pip install fastapi uvicorn langgraph langchain-core --break-system-packages
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


# ---------------------------
# 1. Define the LangGraph State
# ---------------------------
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    bot_response: str


# ---------------------------
# 2. Define Graph Nodes
# ---------------------------
def process_input(state: ChatState) -> ChatState:
    """Node 1: Process / clean the user input."""
    text = state["user_input"].strip()
    state["user_input"] = text
    return state


def generate_response(state: ChatState) -> ChatState:
    """
    Node 2: Generate a response.
    Replace this simple logic with an LLM call (e.g., ChatOpenAI, ChatAnthropic)
    or with a RAG retrieval node on Day 2.
    """
    user_text = state["user_input"].lower()

    if "hello" in user_text or "hi" in user_text:
        response = "Hello! I'm your NetSol assistant. How can I help you today?"
    elif "netsol" in user_text:
        response = "NetSol Technologies is a global provider of software and IT services for the financial industry."
    elif "bye" in user_text:
        response = "Goodbye! Have a great day."
    else:
        response = f"You said: '{state['user_input']}'. (This is a placeholder response — connect an LLM or RAG pipeline here.)"

    state["bot_response"] = response
    return state


# ---------------------------
# 3. Build the Graph
# ---------------------------
def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("process_input", process_input)
    graph.add_node("generate_response", generate_response)

    graph.set_entry_point("process_input")
    graph.add_edge("process_input", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


chat_graph = build_graph()


# ---------------------------
# 4. FastAPI App
# ---------------------------
app = FastAPI(title="NetSol Chatbot API")

# Allow frontend (served from file:// or localhost) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"status": "ok", "message": "NetSol Chatbot API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    initial_state: ChatState = {
        "messages": [],
        "user_input": request.message,
        "bot_response": "",
    }

    result = chat_graph.invoke(initial_state)

    return ChatResponse(response=result["bot_response"])
