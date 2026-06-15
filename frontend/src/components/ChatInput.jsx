import React, { useState } from "react";

/**
 * Input box + send button for composing chat messages.
 * @param {function} onSend - callback called with the message text when sent
 * @param {boolean} disabled - disables input while waiting for a response
 */
function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Type a message..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={disabled}
        autoComplete="off"
      />
      <button onClick={handleSend} disabled={disabled}>
        Send
      </button>
    </div>
  );
}

export default ChatInput;
