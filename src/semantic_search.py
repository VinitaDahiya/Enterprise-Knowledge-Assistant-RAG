
import logging
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model():
    """
    Load and cache the embedding model.

    The model is loaded only once during the lifetime
    of the Python process.
    """
    logger.info("Loading embedding model.")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


@lru_cache(maxsize=1)
def get_collection():
    """
    Connect to and cache the existing ChromaDB collection.

    The collection connection is created only once during
    the lifetime of the Python process.
    """
    logger.info("Connecting to ChromaDB.")

    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        collection = client.get_collection(name="enterprise_knowledge" )
        logger.info("Existing ChromaDB collection found.")
        return collection
    
    except Exception:
        logger.info("ChromaDB collection not found. Building vector store...")
        from src.vector_store import create_vector_store

        collection = create_vector_store()
        logger.info("ChromaDB vector store created successfully.")
        return collection
        

    


def search_documents(query, top_k=3):
    """
    Search ChromaDB for the most relevant document chunks.

    Includes:
    - Query validation
    - top_k validation
    - Cached embedding model
    - Cached ChromaDB collection
    - Retrieval error handling
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    try:
        model = get_embedding_model()
        collection = get_collection()

        query_embedding = model.encode([query])[0]

        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        return results

    except Exception as e:
        logger.error("Retrieval error: %s", e)

        return None


if __name__ == "__main__":

    query = "How many annual leave days do employees receive?"

    results = search_documents(query)

    print("\nSearch Results:\n")

    for i in range(len(results["documents"][0])):

        document = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        print(f"Result {i + 1}")
        print("=" * 80)

        print("Document:")
        print(document)

        print("\nSource:")
        print(metadata.get("source"))

        print("Page:")
        print(metadata.get("page"))

        print("Distance:")
        print(distance)

        print("-" * 80)