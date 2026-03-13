from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.llm import generate_response
from app.core.embeddings import create_embedding
from app.core.vectorstore import add_texts_with_embeddings, search
from app.core.retriever import rag_answer
from app.api.upload import router as upload_router
from app.core.vectorstore import reset_index
from app.core.vectorstore import load_index


app = FastAPI(title="Enterprise AI Copilot")
load_index()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/test-llm")
def test_llm():
    reply = generate_response(
        "Explain Retrieval Augmented Generation (RAG) in AI in simple terms."
    )
    return {"response": reply}

@app.get("/test-vector")
def test_vector():

    docs = [
        "RAG stands for Retrieval Augmented Generation in AI.",
        "FastAPI is a modern Python web framework.",
        "FAISS is used for similarity search in vector databases."
    ]

    embeddings = [create_embedding(doc) for doc in docs]

    add_texts_with_embeddings(docs, embeddings)

    query_embedding = create_embedding("What is RAG in AI?")

    results = search(query_embedding)

    return {"results": results}

@app.get("/rag")
def rag(question: str, provider: str = None):
    return rag_answer(question, provider)

app.include_router(upload_router)

@app.get("/chat")
def chat(question: str, provider: str = None):
    from app.core.llm import generate_response

    answer = generate_response(question, provider)
    return {"answer": answer}

@app.post("/clear")
def clear_index():
    reset_index()
    return {"message": "Vector index cleared successfully"}