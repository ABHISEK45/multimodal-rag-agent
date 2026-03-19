import React, { useState } from "react";
import "./App.css";

const backend = "http://127.0.0.1:8000"; // change later for deployment

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [provider, setProvider] = useState("gemini");
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {
    if (!file) return alert("Select a file first");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    await fetch(`${backend}/upload`, {
      method: "POST",
      body: formData,
    });

    setLoading(false);
    alert("Document uploaded!");
  };

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);

    const res = await fetch(
      `${backend}/rag?question=${question}&provider=${provider}`
    );
    const data = await res.json();

    setAnswer(data.answer);
    setLoading(false);
  };

  const clearDB = async () => {
    await fetch(`${backend}/clear`, { method: "POST" });
    alert("Database cleared!");
  };

  return (
    <div className="container">
      <h1>🧠 Multimodal RAG Agent</h1>

      <div className="card">
        <h2>📂 Upload Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile}>Upload</button>
      </div>

      <div className="card">
        <h2>💬 Ask Question</h2>

        <select
          value={provider}
          onChange={(e) => setProvider(e.target.value)}
        >
          <option value="gemini">Gemini</option>
          <option value="claude">Claude</option>
          <option value="openai">OpenAI</option>
          <option value="ollama">Ollama</option>
        </select>

        <input
          type="text"
          placeholder="Ask something..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={askQuestion}>Ask</button>
      </div>

      <div className="card">
        <h2>🧾 Answer</h2>
        {loading ? (
          <p>⏳ Generating response...</p>
        ) : (
          <p>{answer}</p>
        )}
      </div>

      <button className="clear-btn" onClick={clearDB}>
        🗑 Clear Database
      </button>
    </div>
  );
}

export default App;