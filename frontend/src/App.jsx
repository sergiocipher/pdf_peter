import { useState } from "react";
import UploadBox from "./components/UploadBox";
import ChatBox from "./components/ChatBox";
import "./App.css";

function App() {
  const [pdfLoaded, setPdfLoaded] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleUploadSuccess = (data) => {
    setPdfLoaded(true);
    setUploadStatus(data);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📚 NotebookLM Clone</h1>
          <p>Ask questions about your PDF documents using AI</p>
        </div>
      </header>

      <main className="app-main">
        <section className="upload-section">
          <UploadBox onUploadSuccess={handleUploadSuccess} />
        </section>

        <section className="chat-section">
          <ChatBox pdfLoaded={pdfLoaded} uploadStatus={uploadStatus} />
        </section>
      </main>

      <footer className="app-footer">
        <p>&copy; 2026 RAG NotebookLM | Powered by FastAPI & React</p>
      </footer>
    </div>
  );
}

export default App;