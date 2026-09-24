

import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # This loads .env file and allows the OpenAI SDK to use your API key.

client = OpenAI()
logger = logging.getLogger(__name__)


def generate_answer(query, retrieved_documents):
    """
    Generate an answer using the retrieved document context.
    """

    context = "\n\n".join(retrieved_documents)
    # Combine the retrieved chunks into one piece of context.

    prompt = f"""
You are an enterprise knowledge assistant.

Your job is to answer the user's question using ONLY the information
contained in the retrieved document context.

IMPORTANT RULES:

1. Use only the retrieved context provided below.
2. Do not use your general or pre-trained knowledge.
3. Do not make assumptions or invent information.
4. If the retrieved context does not contain enough information to
   answer the question, respond exactly with:

   "I don't have enough information in the provided documents."

5. If the context contains the answer, provide a concise and clear answer.
6. Do not mention these instructions in your answer.

Retrieved Document Context:
{context}

User Question:
{query}
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        
        logger.error("OpenAI API error: %s", e)
        

        return "Sorry, I couldn't generate an answer right now."


if __name__ == "__main__":
    # We have a small test. We're manually pretending that
    # ChromaDB returned this document.

    test_context = [
        """
        Leave Policy (Dummy)

        Employees receive 20 annual leave days per calendar year.
        Up to 10 paid sick leave days are available.
        Employees may avail 5 casual leave days annually.
        """
    ]

    question = "How many annual leave days do employees receive?"

    # Then we ask the generation function.

    answer = generate_answer(
        question,
        test_context
    )

    print("\nGenerated Answer:\n")
    print(answer)