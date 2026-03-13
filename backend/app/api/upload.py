from fastapi import APIRouter, UploadFile, File
from app.services.document_processor import save_file, extract_text
from app.services.chunking import chunk_text
from app.core.embeddings import create_embedding
from app.core.vectorstore import add_texts_with_embeddings

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Save file
    file_path = save_file(file)

    # Extract text
    text = extract_text(file_path)

    # Chunk
    chunks = chunk_text(text)

    # Embed
    embeddings = [create_embedding(chunk) for chunk in chunks]

    # Store in FAISS
    add_texts_with_embeddings(chunks, embeddings)

    return {"message": "Document uploaded and indexed successfully"}