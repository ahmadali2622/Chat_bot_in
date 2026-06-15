import React, { useEffect, useRef } from "react";
import Message from "./Message.jsx";

/**
 * Scrollable list of chat messages, auto-scrolls to bottom on update.
 * @param {Array<{text: string, sender: "user"|"bot"}>} messages
 * @param {boolean} isTyping - shows a "Bot is typing..." indicator
 */
function ChatWindow({ messages, isTyping }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="chat-messages">
      {messages.map((msg, idx) => (
        <Message key={idx} text={msg.text} sender={msg.sender} />
      ))}
      {isTyping && <div className="typing">Bot is typing...</div>}
      <div ref={bottomRef} />
    </div>
  );
}

export default ChatWindow;
