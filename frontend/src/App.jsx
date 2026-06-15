import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import ChatInput from "./components/ChatInput.jsx";

// Change this if your backend runs on a different host/port
const API_URL = "http://127.0.0.1:8000/chat";

function App() {
  const [messages, setMessages] = useState([
    { text: "Hi! Ask me anything — I'm powered by Gemini 2.5 Flash-Lite.", sender: "bot" },
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (text) => {
    // Add user message immediately
    setMessages((prev) => [...prev, { text, sender: "user" }]);
    setIsTyping(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.reply, sender: "bot" }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { text: "⚠️ Error connecting to server. Is the backend running?", sender: "bot" },
      ]);
      console.error(err);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">NetSol Chatbot</div>
      <ChatWindow messages={messages} isTyping={isTyping} />
      <ChatInput onSend={handleSend} disabled={isTyping} />
    </div>
  );
}

export default App;
