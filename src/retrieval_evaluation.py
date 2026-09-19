from semantic_search import search_documents


evaluation_dataset = [
    {
        "question": "How many annual leave days do employees receive?",
        "expected_source": "Leave_Policy_Dummy.pdf"
    },
    {
        "question": "How many paid sick leave days are available?",
        "expected_source": "Leave_Policy_Dummy.pdf"
    },
    {
        "question": "What are the standard working hours?",
        "expected_source": "HR_Policy_Dummy.pdf"
    },
    {
        "question": "How do employees request leave?",
        "expected_source": "Leave_Policy_Dummy.pdf"
    },
    {
        "question": "Who is Alice?",
        "expected_source": "alicesadventurescarroll.pdf"
    }
]


def evaluate_retrieval(top_k):
    """
    Evaluate retrieval performance at Top-K.

    For each question, check:
    - Whether the expected source was retrieved
    - The rank of the first matching result
    - The distance of the first matching result
    """

    correct = 0

    print("\n" + "=" * 80)
    print(f"RETRIEVAL EVALUATION - RECALL@{top_k}")
    print("=" * 80)

    for item in evaluation_dataset:

        question = item["question"]
        expected_source = item["expected_source"]

        results = search_documents(
            question,
            top_k=top_k
        )

        retrieved_sources = results["metadatas"][0]
        distances = results["distances"][0]

        matching_rank = None
        matching_distance = None

        for rank, metadata in enumerate(
            retrieved_sources,
            start=1
        ):

            source = metadata.get("source", "")

            if expected_source in source:
                matching_rank = rank
                matching_distance = distances[rank - 1]
                break

        if matching_rank is not None:
            correct += 1

        print("\nQuestion:")
        print(question)

        print("\nExpected Source:")
        print(expected_source)

        print("\nFirst Matching Result:")

        if matching_rank is not None:
            print(f"Rank: {matching_rank}")
            print(f"Distance: {matching_distance:.4f}")
            print("Retrieved: True")
        else:
            print("Rank: Not found")
            print("Distance: Not available")
            print("Retrieved: False")

    recall = correct / len(evaluation_dataset)

    print("\n" + "=" * 80)
    print(f"Correct: {correct}/{len(evaluation_dataset)}")
    print(f"Recall@{top_k}: {recall:.2%}")
    print("=" * 80)

    return recall




if __name__ == "__main__":

    evaluate_retrieval(top_k=1)   #this asks: Is the correct document the #1 result? That's Recall@1

    evaluate_retrieval(top_k=3)   #asks: Is the correct document somewhere in the top 3?That's Recall@3

    evaluate_retrieval(top_k=5)   #asks: Is the correct document somewhere in the top 5?That's Recall@5