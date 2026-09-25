from sentence_transformers import SentenceTransformer
from src.text_splitter import create_chunks


def generate_embeddings():
    """
    Generate embeddings for all document chunks.
    """

    # Create chunks
    chunks = create_chunks()

    # Load the embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Extract text from all chunks
    chunk_texts = [chunk.page_content for chunk in chunks]

    # Generate embeddings
    embeddings = model.encode(chunk_texts)

    return chunks, embeddings