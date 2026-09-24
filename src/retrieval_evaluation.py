from semantic_search import search_documents


# =========================================================
# Evaluation Dataset
# =========================================================

evaluation_dataset = [

    # -----------------------------------------------------
    # Answerable questions
    # -----------------------------------------------------

    {
        "question": "How many annual leave days do employees receive?",
        "expected_source": "Leave_Policy_Dummy.pdf",
        "answerable": True
    },

    {
        "question": "How many paid sick leave days are available?",
        "expected_source": "Leave_Policy_Dummy.pdf",
        "answerable": True
    },

    {
        "question": "What are the standard working hours?",
        "expected_source": "HR_Policy_Dummy.pdf",
        "answerable": True
    },

    {
        "question": "How do employees request leave?",
        "expected_source": "Leave_Policy_Dummy.pdf",
        "answerable": True
    },

    {
        "question": "Who is Alice?",
        "expected_source": "alicesadventurescarroll.pdf",
        "answerable": True
    },

    # -----------------------------------------------------
    # Unanswerable questions
    # -----------------------------------------------------

    {
        "question": "What is the company's maternity leave policy?",
        "expected_source": None,
        "answerable": False
    },

    {
        "question": "What is the company's relocation allowance?",
        "expected_source": None,
        "answerable": False
    },

    {
        "question": "What is the company's dental insurance coverage?",
        "expected_source": None,
        "answerable": False
    }
]


# =========================================================
# Retrieval Evaluation
# =========================================================

def evaluate_retrieval(top_k):
    """
    Evaluate retrieval performance at Top-K.

    For answerable questions:
    - Check whether the expected source was retrieved.
    - Record the rank of the first matching result.
    - Record the distance of the first matching result.

    For unanswerable questions:
    - No expected source is required.
    - Retrieval results are displayed for inspection.
    """

    correct = 0
    answerable_questions = 0

    print("\n" + "=" * 80)
    print(f"RETRIEVAL EVALUATION - RECALL@{top_k}")
    print("=" * 80)

    for item in evaluation_dataset:

        question = item["question"]
        expected_source = item["expected_source"]
        answerable = item["answerable"]

        results = search_documents(
            question,
            top_k=top_k
        )

        if results is None:

            print("\nQuestion:")
            print(question)

            print("\nRetrieval failed.")

            continue

        retrieved_sources = results["metadatas"][0]
        distances = results["distances"][0]

        matching_rank = None
        matching_distance = None

        # -------------------------------------------------
        # Answerable question
        # -------------------------------------------------

        if answerable:

            answerable_questions += 1

            for rank, metadata in enumerate(
                retrieved_sources,
                start=1
            ):

                source = metadata.get(
                    "source",
                    ""
                )

                if expected_source in source:

                    matching_rank = rank
                    matching_distance = distances[rank - 1]

                    break

            if matching_rank is not None:

                correct += 1

        # -------------------------------------------------
        # Display question
        # -------------------------------------------------

        print("\nQuestion:")
        print(question)

        # -------------------------------------------------
        # Display expected source
        # -------------------------------------------------

        print("\nExpected Source:")

        if expected_source is not None:

            print(expected_source)

        else:

            print(
                "No source expected - "
                "question is intentionally unanswerable."
            )

        # -------------------------------------------------
        # Display retrieval result
        # -------------------------------------------------

        print("\nFirst Matching Result:")

        if matching_rank is not None:

            print(f"Rank: {matching_rank}")
            print(
                f"Distance: {matching_distance:.4f}"
            )
            print("Retrieved: True")

        elif not answerable:

            print(
                "Question is unanswerable."
            )

            print(
                "Retrieved documents:"
            )

            for rank, metadata in enumerate(
                retrieved_sources,
                start=1
            ):

                source = metadata.get(
                    "source",
                    "Unknown source"
                )

                distance = distances[rank - 1]

                print(
                    f"{rank}. {source} "
                    f"(Distance: {distance:.4f})"
                )

        else:

            print("Rank: Not found")
            print("Distance: Not available")
            print("Retrieved: False")

    # =====================================================
    # Recall Calculation
    # =====================================================

    if answerable_questions > 0:

        recall = (
            correct / answerable_questions
        )

    else:

        recall = 0

    print("\n" + "=" * 80)

    print(
        f"Correct: {correct}/{answerable_questions}"
    )

    print(
        f"Recall@{top_k}: {recall:.2%}"
    )

    print("=" * 80)

    return recall


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    evaluate_retrieval(top_k=1)

    evaluate_retrieval(top_k=3)

    evaluate_retrieval(top_k=5)