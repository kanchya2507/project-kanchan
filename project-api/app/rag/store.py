import hashlib
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from app.rag.config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformer:
    # The embedding model runs locally; it does not send PDF text to an API.
    return SentenceTransformer(EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def get_collection():
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    """Split extracted PDF text into overlapping chunks."""
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


def add_pdf_pages(source: str, pages: list[tuple[int, str]]) -> int:
    """Embed and save the pages for one PDF, replacing its previous index."""
    collection = get_collection()
    collection.delete(where={"source": source})

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict] = []

    for page_number, text in pages:
        for chunk_number, chunk in enumerate(split_text(text)):
            chunk_id = hashlib.sha256(
                f"{source}:{page_number}:{chunk_number}:{chunk}".encode("utf-8")
            ).hexdigest()

            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append(
                {
                    "source": source,
                    "page": page_number,
                    "chunk": chunk_number,
                }
            )

    if not documents:
        return 0

    embeddings = get_embedder().encode(
        documents,
        normalize_embeddings=True,
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    return len(documents)


def search(query: str, source: str | None = None) -> list[dict]:
    """Return the most relevant stored chunks for a query."""
    collection = get_collection()
    count = collection.count()

    if count == 0:
        return []

    query_embedding = get_embedder().encode(
        [query],
        normalize_embeddings=True,
    ).tolist()

    options = {
        "query_embeddings": query_embedding,
        "n_results": min(TOP_K, count),
        "include": ["documents", "metadatas"],
    }
    if source:
        options["where"] = {"source": source}

    result = collection.query(**options)
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]

    return [
        {"text": document, "metadata": metadata}
        for document, metadata in zip(documents, metadatas)
    ]