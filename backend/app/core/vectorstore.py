import faiss
import numpy as np
import os
import json

# Dimension for all-MiniLM-L6-v2
dimension = 384

# Initialize FAISS index
index = faiss.IndexFlatL2(dimension)

# Store original texts
stored_texts = []

STORAGE_DIR = "storage"
INDEX_PATH = os.path.join(STORAGE_DIR, "faiss.index")
TEXTS_PATH = os.path.join(STORAGE_DIR, "texts.json")

def add_documents(text_chunks: list):
    """
    Adds list of text chunks to FAISS index.
    """
    global stored_texts

    embeddings = np.array(text_chunks, dtype="float32")
    index.add(embeddings)


def add_texts_with_embeddings(texts: list, embeddings: list):
    """
    Store texts + embeddings
    """
    global stored_texts

    vectors = np.array(embeddings, dtype="float32")
    index.add(vectors)
    stored_texts.extend(texts)
    save_index()


def search(query_embedding, top_k=3):
    """
    Search most similar chunks
    """
    if index.ntotal == 0:
        return []

    query_vector = np.array([query_embedding], dtype="float32")
    distances, indices = index.search(query_vector, top_k)

    results = []

    for idx in indices[0]:
        # Skip invalid indices
        if idx == -1:
            continue
        if idx < len(stored_texts):
            results.append(stored_texts[idx])

    return results

def reset_index():
    global index, stored_texts

    index = faiss.IndexFlatL2(dimension)
    stored_texts = []

    # Remove stored files
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)

    if os.path.exists(TEXTS_PATH):
        os.remove(TEXTS_PATH)

    return True


def save_index():
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    faiss.write_index(index, INDEX_PATH)

    with open(TEXTS_PATH, "w", encoding="utf-8") as f:
        json.dump(stored_texts, f)


def load_index():
    global index, stored_texts

    try:
        if (
            os.path.exists(INDEX_PATH)
            and os.path.exists(TEXTS_PATH)
            and os.path.getsize(INDEX_PATH) > 0
        ):
            index = faiss.read_index(INDEX_PATH)

            with open(TEXTS_PATH, "r", encoding="utf-8") as f:
                stored_texts = json.load(f)

            print("✅ FAISS index loaded from disk")

        else:
            print("⚠️ No valid index found, starting fresh")

    except Exception as e:
        print("⚠️ Failed to load FAISS index, starting fresh")
        print(e)

        index = faiss.IndexFlatL2(dimension)
        stored_texts = []