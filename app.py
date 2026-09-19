import os

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
# Header
# ---------------------------------------------------------

st.title("📚 Enterprise Knowledge Assistant")

st.markdown(
    "Ask questions and get answers grounded in the information "
    "contained in the enterprise documents."
)

st.caption(
    "Powered by semantic search, ChromaDB, and an OpenAI language model."
)


# ---------------------------------------------------------
# Question input
# ---------------------------------------------------------

st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Example: How many annual leave days do employees receive?",
    label_visibility="visible"
)


# ---------------------------------------------------------
# Ask button
# ---------------------------------------------------------

if st.button("Ask Question", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Searching the knowledge base and generating an answer..."
        ):

            answer, results = ask_question(
                question,
                top_k=3
            )

        # -------------------------------------------------
        # Answer
        # -------------------------------------------------

        st.divider()

        st.subheader("💡 Answer")

        st.write(answer)

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        if results is not None:

            st.subheader("📄 Sources")

            for i in range(len(results["metadatas"][0])):

                metadata = results["metadatas"][0][i]

                source = metadata.get(
                    "source",
                    "Unknown source"
                )

                # Display only the filename instead of the
                # complete local file path.
                filename = os.path.basename(source)

                page = metadata.get("page")

                if page is not None:
                    page = page + 1

                st.write(
                    f"**{i + 1}. {filename}** — Page {page}"
                )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Answers are generated using retrieved document context. "
    "If the required information is not available in the "
    "provided documents, the assistant may decline to answer."
)