import { useState } from "react";
import API from "../services/api";
import "./UploadBox.css";

function UploadBox({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF file");
      setStatus("error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setStatus("loading");

    try {
      const response = await API.post("/uploads", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage(`✓ PDF uploaded successfully!
Pages: ${response.data.total_pages} | Chunks: ${response.data.total_chunks}`);
      setStatus("success");
      onUploadSuccess(response.data);
      setFile(null);
    } catch (error) {
      console.error("Upload failed:", error);
      setMessage(
        error.response?.data?.detail || "Upload failed. Please try again."
      );
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-box">
      <h2>📤 Upload PDF Document</h2>

      <div className="upload-input-group">
        <label htmlFor="file-input" className="file-input-label">
          {file ? `Selected: ${file.name}` : "Choose a PDF file"}
        </label>
        <input
          id="file-input"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="file-input"
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={loading || !file}
        className="upload-btn"
      >
        {loading ? "Uploading..." : "Upload PDF"}
      </button>

      {message && (
        <div className={`message ${status}`}>
          {message}
        </div>
      )}
    </div>
  );
}

export default UploadBox;