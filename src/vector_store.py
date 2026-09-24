import chromadb

from embeddings import generate_embeddings


def create_vector_store():
    """
    Generate embeddings and store document chunks in ChromaDB.
    """

    # Generate document chunks and embeddings
    chunks, embeddings = generate_embeddings()

    # Create a persistent ChromaDB client
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    # Create or get the collection
    collection = client.get_or_create_collection(
        name="enterprise_knowledge"
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

    # Add new records or update existing records
    collection.upsert(
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