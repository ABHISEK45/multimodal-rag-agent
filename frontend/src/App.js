import React, { useState } from "react";

function App() {

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [provider, setProvider] = useState("gemini");

  const backend = "http://127.0.0.1:8000";

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${backend}/upload`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    alert(data.message);
  };

  const askQuestion = async () => {
    if (!question) return;

    const res = await fetch(
      `${backend}/rag?question=${encodeURIComponent(question)}&provider=${provider}`
    );

    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Enterprise AI Copilot</h1>

      <h3>Upload Document</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload</button>

      <hr />

      <h3>Ask Question</h3>

      <label>Provider:</label>
      <select
        value={provider}
        onChange={(e) => setProvider(e.target.value)}
      >
        <option value="gemini">Gemini</option>
        <option value="claude">Claude</option>
        <option value="openai">OpenAI</option>
        <option value="ollama">Ollama</option>
      </select>

      <br /><br />

      <input
        type="text"
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "400px", padding: "8px" }}
      />

      <button onClick={askQuestion} style={{ marginLeft: "10px" }}>
        Ask
      </button>

      <hr />

      <h3>Answer</h3>
      <p>{answer}</p>
    </div>
  );
}

export default App;