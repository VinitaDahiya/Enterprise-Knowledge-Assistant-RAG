import streamlit as st

from src.rag_pipeline import ask_question


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📚",
    layout="centered"
)


# ---------------------------------------------------------
# Application title
# ---------------------------------------------------------

st.title("📚 Enterprise Knowledge Assistant")

st.write(
    "Ask questions about the information contained in the "
    "uploaded enterprise documents."
)


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

question = st.text_input(
    "Ask a question:",
    placeholder="Example: How many annual leave days do employees receive?"
)


# ---------------------------------------------------------
# Ask button
# ---------------------------------------------------------

if st.button("Ask Question"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching documents and generating answer..."):

            answer, results = ask_question(
                question,
                top_k=3
            )

        # -------------------------------------------------
        # Display answer
        # -------------------------------------------------

        st.subheader("Answer")

        st.write(answer)

        # -------------------------------------------------
        # Display sources
        # -------------------------------------------------

        if results is not None:

            st.subheader("Sources")

            for i in range(len(results["metadatas"][0])):

                metadata = results["metadatas"][0][i]

                source = metadata.get(
                    "source",
                    "Unknown source"
                )

                page = metadata.get("page")

                if page is not None:
                    page = page + 1

                st.write(
                    f"{i + 1}. {source} — Page {page}"
                )