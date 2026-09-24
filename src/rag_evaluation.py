from src.rag_pipeline import ask_question


# =========================================================
# Evaluation Dataset
# =========================================================

evaluation_dataset = [

    # -----------------------------------------------------
    # Answerable questions
    # -----------------------------------------------------

    {
        "question": "How many annual leave days do employees receive?",
        "expected_keywords": [
            "20",
            "annual leave"
        ],
        "answerable": True
    },

    {
        "question": "How many paid sick leave days are available?",
        "expected_keywords": [
            "10",
            "sick leave"
        ],
        "answerable": True
    },

    {
        "question": "What are the standard working hours?",
        "expected_keywords": [
            "9:00",
            "6:00"
        ],
        "answerable": True
    },

    {
        "question": "How do employees request leave?",
        "expected_keywords": [
            "leave",
            "manager"
        ],
        "answerable": True
    },

    {
        "question": "Who is Alice?",
        "expected_keywords": [
            "Alice"
        ],
        "answerable": True
    },

    # -----------------------------------------------------
    # Unanswerable questions
    # -----------------------------------------------------

    {
        "question": "What is the company's maternity leave policy?",
        "expected_keywords": [],
        "answerable": False
    },

    {
        "question": "What is the company's relocation allowance?",
        "expected_keywords": [],
        "answerable": False
    },

    {
        "question": "What is the company's dental insurance coverage?",
        "expected_keywords": [],
        "answerable": False
    }
]


# =========================================================
# Expected Abstention Response
# =========================================================

ABSTENTION_RESPONSE = (
    "I don't have enough information in the provided documents."
)


# =========================================================
# Evaluation Function
# =========================================================

def evaluate_rag():
    """
    Evaluate the complete RAG pipeline.

    For answerable questions:
    - Verify that an answer is generated.
    - Check whether expected keywords appear.

    For unanswerable questions:
    - Verify that the system returns the expected
      abstention response.
    """

    answerable_correct = 0
    answerable_total = 0

    abstention_correct = 0
    abstention_total = 0

    print("\n" + "=" * 80)
    print("END-TO-END RAG EVALUATION")
    print("=" * 80)

    for item in evaluation_dataset:

        question = item["question"]
        expected_keywords = item["expected_keywords"]
        answerable = item["answerable"]

        print("\n" + "-" * 80)
        print("Question:")
        print(question)

        # -------------------------------------------------
        # Run complete RAG pipeline
        # -------------------------------------------------

        answer, results = ask_question(
            question,
            top_k=3
        )

        print("\nGenerated Answer:")
        print(answer)

        # -------------------------------------------------
        # Answerable question
        # -------------------------------------------------

        if answerable:

            answerable_total += 1

            answer_lower = answer.lower()

            keywords_found = all(
                keyword.lower() in answer_lower
                for keyword in expected_keywords
            )

            if keywords_found:

                answerable_correct += 1

                print("\nEvaluation:")
                print("PASS - Expected information found.")

            else:

                print("\nEvaluation:")
                print("FAIL - Expected information not found.")

                print(
                    "\nExpected keywords:"
                )

                print(expected_keywords)

        # -------------------------------------------------
        # Unanswerable question
        # -------------------------------------------------

        else:

            abstention_total += 1

            if answer.strip() == ABSTENTION_RESPONSE:

                abstention_correct += 1

                print("\nEvaluation:")
                print("PASS - System correctly abstained.")

            else:

                print("\nEvaluation:")
                print(
                    "FAIL - System did not abstain correctly."
                )

    # =====================================================
    # Calculate Metrics
    # =====================================================

    if answerable_total > 0:

        answerable_accuracy = (
            answerable_correct / answerable_total
        )

    else:

        answerable_accuracy = 0

    if abstention_total > 0:

        abstention_accuracy = (
            abstention_correct / abstention_total
        )

    else:

        abstention_accuracy = 0

    total_correct = (
        answerable_correct +
        abstention_correct
    )

    total_questions = (
        answerable_total +
        abstention_total
    )

    overall_accuracy = (
        total_correct / total_questions
    )

    # =====================================================
    # Evaluation Summary
    # =====================================================

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)

    print(
        f"Answerable Questions: "
        f"{answerable_correct}/{answerable_total}"
    )

    print(
        f"Answerable Accuracy: "
        f"{answerable_accuracy:.2%}"
    )

    print(
        f"Unanswerable Questions: "
        f"{abstention_correct}/{abstention_total}"
    )

    print(
        f"Abstention Accuracy: "
        f"{abstention_accuracy:.2%}"
    )

    print(
        f"Overall: "
        f"{total_correct}/{total_questions}"
    )

    print(
        f"Overall Accuracy: "
        f"{overall_accuracy:.2%}"
    )

    print("=" * 80)


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    evaluate_rag()