from app.core.embeddings import create_embedding
from app.core.vectorstore import search
from app.core.llm import generate_response


def rag_answer(question, provider=None):

    # 1️⃣ Create embedding for question
    query_embedding = create_embedding(question)

    # 2️⃣ Retrieve relevant chunks
    retrieved_chunks = search(query_embedding, top_k=3)

    # 3️⃣ Build context
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI assistant answering based ONLY on the provided context.

Context:
{context}

Question:
{question}

Answer clearly and cite the relevant information from the context.
"""

    # 4️⃣ Generate response
    answer = generate_response(prompt, provider)

    return {
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }