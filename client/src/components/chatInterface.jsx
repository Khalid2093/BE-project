import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! How can I help you with your legal questions today?",
    },
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]); // Scroll when messages update

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const LlmContent = await axios.post(
      "http://localhost:5000/process_prompt",
      {
        prompt: input,
      }
    );
    console.log(LlmContent.data);

    setMessages((prev) => [
      ...prev,
      { role: "user", content: input },
      {
        role: "assistant",
        content: LlmContent.data.response || "Sorry, I didn't get that.",
      },
    ]);
    setInput("");
  };

  return (
    <div className="chat-container">
      <header className="header">
        <div className="header-content">
          <h1 className="logo">LAWGARITHM</h1>
          <div className="user-menu">
            <div className="user-icon">
              <svg viewBox="0 0 24 24" width="24" height="24">
                <path
                  fill="currentColor"
                  d="M12 4a4 4 0 014 4 4 4 0 01-4 4 4 4 0 01-4-4 4 4 0 014-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4z"
                />
              </svg>
            </div>
          </div>
        </div>
      </header>

      <div className="messages-area">
        {messages.map((message, index) => (
          <div key={index} className={`message-wrapper ${message.role}`}>
            <div className="message-container">
              {message.role === "assistant" && (
                <div className="avatar assistant-avatar">
                  <svg viewBox="0 0 24 24" width="20" height="20">
                    <path
                      fill="currentColor"
                      d="M12 2c5.5 0 10 4.5 10 10s-4.5 10-10 10S2 17.5 2 12 6.5 2 12 2zm0 2c-4.4 0-8 3.6-8 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8zm0 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm-4 9v-1c0-1.1 1.8-2 4-2s4 .9 4 2v1h-8z"
                    />
                  </svg>
                </div>
              )}
              <div className="message-bubble">{message.content}</div>
              {message.role === "user" && (
                <div className="avatar user-avatar">
                  <svg viewBox="0 0 24 24" width="20" height="20">
                    <path
                      fill="currentColor"
                      d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                    />
                  </svg>
                </div>
              )}
            </div>
          </div>
        ))}
        {/* Invisible element to scroll to */}
        <div ref={messagesEndRef} className="scroll-spacer" />
      </div>

      <div className="input-area">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button type="submit">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path
                fill="currentColor"
                d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"
              />
            </svg>
          </button>
        </form>
      </div>

      <style>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background-color: #f5f5f5;
        }

        .header {
          position: sticky;
          top: 0;
          background-color: #2563eb;
          color: white;
          padding: 16px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          z-index: 1000;
        }

        .header-content {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .logo {
          font-size: 24px;
          font-weight: bold;
          margin: 0;
          letter-spacing: 1px;
        }

        .user-menu {
          display: flex;
          align-items: center;
        }

        .user-icon {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background-color: rgba(255, 255, 255, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .user-icon:hover {
          background-color: rgba(255, 255, 255, 0.3);
        }

        .messages-area {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          padding-bottom: 80px;
          scroll-behavior: smooth;
        }

        .message-wrapper {
          display: flex;
          width: 100%;
          margin-bottom: 20px;
          animation: fadeIn 0.3s ease-in-out;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .message-wrapper.user {
          justify-content: flex-end;
        }

        .message-container {
          display: flex;
          align-items: flex-start;
          gap: 8px;
          max-width: 80%;
        }

        .user .message-container {
          flex-direction: row-reverse;
        }

        .message-bubble {
          padding: 12px;
          border-radius: 12px;
          background-color: white;
          position: relative;
          box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        .user .message-bubble {
          background-color: #2563eb;
          color: white;
          border-top-right-radius: 2px;
        }

        .assistant .message-bubble {
          background-color: white;
          border-top-left-radius: 2px;
        }

        .avatar {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .assistant-avatar {
          background-color: #2563eb;
          color: white;
        }

        .user-avatar {
          background-color: #6b7280;
          color: white;
        }

        .input-area {
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          background-color: white;
          padding: 16px;
          border-top: 1px solid #e5e5e5;
          box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
        }

        .input-area form {
          display: flex;
          gap: 8px;
          max-width: 1200px;
          margin: 0 auto;
        }

        .input-area input {
          flex: 1;
          padding: 12px 16px;
          border: 1px solid #e5e5e5;
          border-radius: 8px;
          outline: none;
          font-size: 16px;
        }

        .input-area input:focus {
          border-color: #2563eb;
          box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
        }

        .input-area button {
          padding: 12px 16px;
          background-color: #2563eb;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.2s;
        }

        .input-area button:hover {
          background-color: #1d4ed8;
        }

        .scroll-spacer {
          height: 20px;
        }
      `}</style>
    </div>
  );
};

export default ChatInterface;
