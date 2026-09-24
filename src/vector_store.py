import chromadb

from embeddings import generate_embeddings


COLLECTION_NAME = "enterprise_knowledge"
VECTOR_STORE_PATH = "./chroma_db"


def create_vector_store():
    """
    Build the ChromaDB vector store from the current PDF documents.

    The existing collection is recreated so that deleted or modified
    documents cannot leave stale chunks in the vector store.
    """

    # Generate document chunks and embeddings
    chunks, embeddings = generate_embeddings()

    # Create a persistent ChromaDB client
    client = chromadb.PersistentClient(
        path=VECTOR_STORE_PATH
    )

    # Delete the existing collection if it exists
    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        # Collection does not exist yet
        pass

    # Create a fresh collection
    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    # Prepare data for ChromaDB
    documents = [
        chunk.page_content
        for chunk in chunks
    ]

    metadatas = [
        chunk.metadata
        for chunk in chunks
    ]

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    # Add the current document chunks
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return collection


if __name__ == "__main__":

    collection = create_vector_store()

    print(
        f"Vector store ready. "
        f"Documents in collection: {collection.count()}"
    )