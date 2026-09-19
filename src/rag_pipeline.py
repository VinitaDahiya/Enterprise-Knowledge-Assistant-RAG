import logging
from src.semantic_search import search_documents
from src.llm_generator import generate_answer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def ask_question(query, top_k=3):
    """
    Complete RAG pipeline:
    1. Retrieve relevant document chunks.
    2. Generate an answer using those chunks.
    """
    
    if not query or not query.strip():
        logger.warning("Received an empty query.")
        
        return (
            "Please enter a question.",
            None
        )
        
    logger.info("Received query.")    

    # Step 1: Retrieve relevant documents
    results = search_documents(
    query,
    top_k=top_k
    )

    # Step 2: Handle retrieval failure
    if results is None:
        logger.error("Document retrieval failed.")
        
        return (
        "Sorry, I couldn't retrieve information from the knowledge base right now.",
        None
    )

    # Step 3: Extract the retrieved document text
    retrieved_documents = results["documents"][0]
    
    logger.info(
        "Retrieved %d document chunks.",
        len(retrieved_documents)
    )

    # Step 4: Generate an answer using the retrieved context
    
    logger.info("Generating answer using OpenAI.")
    answer = generate_answer(
        query,
        retrieved_documents
    )
    
    logger.info("Answer generated successfully.")

    return answer, results


if __name__ == "__main__":

    question = "How many annual leave days do employees receive?"

    answer, results = ask_question(
        question,
        top_k=3
    )

    print("\n" + "=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)

    print(answer)

    if results is not None:

        print("\n" + "=" * 80)
        print("SOURCES")
        print("=" * 80)

        for i in range(len(results["metadatas"][0])):

            metadata = results["metadatas"][0][i]

            source = metadata.get("source", "Unknown source")
            page = metadata.get("page")

            if page is not None:
                page = page + 1

            print(f"\n{i + 1}. {source}")
            print(f"   Page: {page}")