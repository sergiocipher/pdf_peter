import { useState, useRef, useEffect } from "react";
import API from "../services/api";
import "./ChatBox.css";

function ChatBox({ pdfLoaded, uploadStatus }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const askQuestion = async (e) => {
    if (e) e.preventDefault(); // Prevent form submission
    
    if (!question.trim()) return;
    if (!pdfLoaded) {
      alert("Please upload a PDF first");
      return;
    }

    const userMsg = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);
    const currentQuestion = question;
    setQuestion("");
    setLoading(true);

    try {
      const response = await API.post("/chat", {
        question: currentQuestion,
      });

      const assistantMsg = { 
        role: "assistant", 
        content: response.data.answer || response.data.response || "No answer received"
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMsg = {
        role: "assistant",
        content: error.response?.data?.detail || error.message || "Failed to get answer. Please try again.",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !loading) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="chat-box">
      <h2>💬 Ask Questions</h2>

      {!pdfLoaded && (
        <div className="no-pdf-message">
          📋 Upload a PDF first to start asking questions
        </div>
      )}

      {uploadStatus && (
        <div className="upload-info">
          <span>✓ PDF loaded</span>
          <span>{uploadStatus.total_pages} pages</span>
          <span>{uploadStatus.total_chunks} chunks</span>
        </div>
      )}

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>👋 Hi! Ask me anything about your PDF document.</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <span className="message-icon">
                {msg.role === "user" ? "👤" : "🤖"}
              </span>
              <div className="message-content">
                {msg.content}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message assistant">
            <span className="message-icon">🤖</span>
            <div className="message-content typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question... (Shift+Enter for new line)"
          disabled={!pdfLoaded || loading}
          className="question-input"
          rows="3"
        />
        <button
          onClick={(e) => askQuestion(e)}
          disabled={!pdfLoaded || loading || !question.trim()}
          className="ask-btn"
          type="button"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default ChatBox;