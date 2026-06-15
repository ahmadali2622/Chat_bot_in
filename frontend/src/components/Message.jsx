import React from "react";

/**
 * Renders a single chat message bubble.
 * @param {string} text - message content
 * @param {"user"|"bot"} sender - who sent the message
 */
function Message({ text, sender }) {
  const isUser = sender === "user";

  return (
    <div className={`message ${isUser ? "user-message" : "bot-message"}`}>
      {text}
    </div>
  );
}

export default Message;
