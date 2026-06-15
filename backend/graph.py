"""
graph.py
--------
LangGraph definition for the chatbot.

Flow:
    START -> chatbot_node -> END

chatbot_node calls Google's Gemini 2.5 Flash-Lite model to generate
a response to the user's message.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL


# ---------------------------
# 1. Configure Gemini Client
# ---------------------------
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# ---------------------------
# 2. Define the State
# ---------------------------
class ChatState(TypedDict):
    user_message: str
    bot_response: str


# ---------------------------
# 3. Define the Node Logic
# ---------------------------
def chatbot_node(state: ChatState) -> ChatState:
    """
    Sends the user's message to Gemini 2.5 Flash-Lite and returns its reply.
    Falls back to an error message if the API call fails
    (e.g. missing API key, network issue, rate limit).
    """
    user_message = state["user_message"]

    if not GEMINI_API_KEY or client is None:
        return {
            "user_message": user_message,
            "bot_response": "⚠️ GEMINI_API_KEY is not set. Please add it to your .env file.",
        }

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_message,
        )
        reply = response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        reply = f"⚠️ Error calling Gemini API: {str(e)}"

    return {"user_message": user_message, "bot_response": reply}


# ---------------------------
# 4. Build the Graph
# ---------------------------
graph_builder = StateGraph(ChatState)
graph_builder.add_node("chatbot_node", chatbot_node)
graph_builder.set_entry_point("chatbot_node")
graph_builder.add_edge("chatbot_node", END)

chat_graph = graph_builder.compile()
