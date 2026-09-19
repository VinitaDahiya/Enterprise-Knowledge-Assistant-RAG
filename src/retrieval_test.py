from semantic_search import search_documents


questions = [
    "How many annual leave days do employees receive?",
    "What is the company's maternity leave policy?"
]


for question in questions:

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    results = search_documents(
        question,
        top_k=3
    )

    print("\nRETRIEVED RESULTS")
    print("=" * 80)

    for i in range(len(results["documents"][0])):

        metadata = results["metadatas"][0][i]

        source = metadata.get("source", "Unknown")
        page = metadata.get("page")
        distance = results["distances"][0][i]
        document_chunk = results["documents"][0][i]

        print(f"\nResult {i + 1}")
        print("-" * 80)

        print("Source:")
        print(source)

        print("\nPage:")
        print(page)

        print("\nDistance:")
        print(f"{distance:.4f}")

        print("\nDocument Chunk:")
        print(document_chunk)