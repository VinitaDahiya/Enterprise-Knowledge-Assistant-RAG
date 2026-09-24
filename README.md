# Enterprise Knowledge Assistant — RAG

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about a collection of enterprise documents and receive answers grounded in the retrieved document context.

The application uses semantic search to retrieve relevant document chunks from a ChromaDB vector store and an OpenAI language model to generate grounded responses.

---

## Project Overview

The Enterprise Knowledge Assistant demonstrates an end-to-end RAG pipeline for querying unstructured PDF documents.

The system:

1. Loads PDF documents from the knowledge base.
2. Splits documents into smaller text chunks.
3. Generates vector embeddings for each chunk.
4. Stores embeddings and document metadata in ChromaDB.
5. Converts a user's question into an embedding.
6. Performs semantic similarity search to retrieve relevant document chunks.
7. Passes the retrieved context to an OpenAI language model.
8. Generates an answer grounded in the retrieved context.
9. Displays the answer along with source documents and page numbers.
10. Abstains when the required information is not available in the provided documents.

---

## Architecture

```text
                     PDF Documents
                          |
                          v
                 Document Loading
                          |
                          v
                   Text Chunking
                          |
                          v
                   Text Embeddings
                (all-MiniLM-L6-v2)
                          |
                          v
                     ChromaDB
                   Vector Store
                          |
                          |
                   User Question
                          |
                          v
                  Query Embedding
                          |
                          v
                  Semantic Search
                          |
                          v
               Top-K Relevant Chunks
                          |
                          v
                 Retrieved Context
                          |
                          v
                    OpenAI LLM
                          |
                          v
                  Grounded Answer
                          |
                   +------+------+
                   |             |
                   v             v
              Source/Page    Abstention
              Attribution     if context
                             is insufficient
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Document Processing | LangChain Community |
| PDF Loading | PyPDFLoader |
| Text Splitting | RecursiveCharacterTextSplitter |
| Embedding Model | SentenceTransformers — `all-MiniLM-L6-v2` |
| Embedding Dimension | 384 |
| Vector Database | ChromaDB |
| LLM | OpenAI API |
| Application UI | Streamlit |
| Environment Management | python-dotenv |
| Version Control | Git |

---

## RAG Pipeline

### 1. Document Loading

PDF files are loaded from:

```text
data/pdfs/
```

The application uses `PyPDFLoader` through LangChain's document loading utilities.

Each PDF page is represented as a document object with metadata such as:

- source file
- page number
- document title
- author
- total pages

---

### 2. Text Chunking

Documents are split into smaller chunks using:

```text
RecursiveCharacterTextSplitter
```

Current configuration:

```text
chunk_size = 1000
chunk_overlap = 200
```

Chunking allows the retrieval system to search smaller, more relevant pieces of the documents instead of passing entire documents to the language model.

---

### 3. Embeddings

Each document chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The embedding dimension is:

```text
384
```

These vectors represent the semantic meaning of the document chunks and allow the system to perform semantic similarity search.

---

### 4. Vector Storage

The generated embeddings are stored in:

```text
ChromaDB
```

The project uses a persistent ChromaDB collection named:

```text
enterprise_knowledge
```

The vector store also maintains the original document text and metadata associated with each chunk.

---

### 5. Semantic Retrieval

When a user asks a question:

1. The question is converted into an embedding.
2. ChromaDB searches for semantically similar document chunks.
3. The top-K results are returned.
4. The retrieved chunks become the context supplied to the language model.

The current application uses:

```text
top_k = 3
```

for the main RAG pipeline.

---

### 6. Grounded Answer Generation

The retrieved document chunks are passed to an OpenAI language model.

The generation prompt instructs the model to:

- use only the retrieved document context
- avoid using general knowledge
- avoid making assumptions
- avoid inventing information
- provide a concise answer when the context contains the required information

If the retrieved context does not contain enough information, the system instructs the model to respond with:

```text
I don't have enough information in the provided documents.
```

---

## Source Attribution

The application displays the source documents used during retrieval.

For example:

```text
1. Leave_Policy_Dummy.pdf — Page 1
2. HR_Policy_Dummy.pdf — Page 1
3. Learning+Hand+Book+-+DS.pdf — Page 1
```

This provides traceability into the documents used by the RAG pipeline.

---

## Handling Unsupported Questions

A semantic retriever returns the nearest available chunks even when the knowledge base does not contain the answer.

To address this, the generation prompt instructs the LLM to abstain when the retrieved context does not contain sufficient information.

For example:

**Question:**

```text
What is the company's maternity leave policy?
```

**Response:**

```text
I don't have enough information in the provided documents.
```

The same abstention behavior was tested for unsupported questions involving:

- maternity leave
- relocation allowance
- dental insurance coverage

---

## Evaluation

The project includes two levels of evaluation.

### Retrieval Evaluation

`src/retrieval_evaluation.py` evaluates whether the expected source document is retrieved for answerable questions.

The evaluation measures:

```text
Recall@1
Recall@3
Recall@5
```

The current evaluation dataset contains:

- 5 answerable questions
- 3 intentionally unanswerable questions

For the 5 answerable questions in the current evaluation set, the expected source document was retrieved at rank 1.

Therefore, the current evaluation produced:

```text
Recall@1: 100%
Recall@3: 100%
Recall@5: 100%
```

These results are based only on the current evaluation dataset and should not be interpreted as a universal retrieval accuracy guarantee.

---

### End-to-End RAG Evaluation

`src/rag_evaluation.py` evaluates the complete RAG pipeline:

```text
Question
   ↓
Retrieval
   ↓
Context
   ↓
LLM Generation
   ↓
Final Answer
```

The evaluation checks:

**For answerable questions**

- whether the expected information appears in the generated answer

**For unanswerable questions**

- whether the system correctly returns the abstention response

Current evaluation result:

```text
Answerable Questions: 5/5
Answerable Accuracy: 100.00%

Unanswerable Questions: 3/3
Abstention Accuracy: 100.00%

Overall: 8/8
Overall Accuracy: 100.00%
```

These results are based on the current 8-question evaluation dataset and should not be interpreted as a universal accuracy guarantee.

---

## Streamlit Application

The project includes a Streamlit interface for interacting with the RAG system.

The application allows users to:

- enter a natural-language question
- retrieve relevant document context
- generate a grounded answer
- view source documents
- view source page numbers
- receive an abstention response when sufficient information is unavailable

Run the application with:

```bash
streamlit run app.py
```

---

## Project Structure

```text
Enterprise-Knowledge-Assistant-RAG/
│
├── app.py
├── config.py
├── README.md
├── requirements.txt
│
├── data/
│   └── pdfs/
│       └── *.pdf
│
├── chroma_db/
│   └── ChromaDB persistent storage
│
└── src/
    ├── document_loader.py
    ├── text_splitter.py
    ├── embeddings.py
    ├── vector_store.py
    ├── semantic_search.py
    ├── llm_generator.py
    ├── rag_pipeline.py
    ├── retrieval_test.py
    ├── retrieval_evaluation.py
    ├── rag_evaluation.py
    └── openai_test.py
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Enterprise-Knowledge-Assistant-RAG
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the OpenAI API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to Git.

### 6. Build the Vector Store

Generate embeddings from the PDF documents and create or update the ChromaDB vector store:

```bash
python src/vector_store.py
```

This creates or updates the persistent ChromaDB collection:

```text
enterprise_knowledge
```

The vector store is stored locally in:

```text
chroma_db/
```

The ingestion process uses `upsert`, so existing document chunks can be updated without creating duplicate IDs.

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will start a local Streamlit server.

---

## Running Evaluation

### Retrieval evaluation

```bash
python src/retrieval_evaluation.py
```

### End-to-end RAG evaluation

```bash
python -m src.rag_evaluation
```

---

## Example Questions

The current knowledge base can answer questions such as:

```text
How many annual leave days do employees receive?
```

```text
How many paid sick leave days are available?
```

```text
What are the standard working hours?
```

```text
How do employees request leave?
```

The evaluation dataset also includes intentionally unsupported questions for testing abstention behavior.

---

## Error Handling

The application includes handling for several failure scenarios, including:

- empty user queries
- document retrieval failures
- OpenAI API failures
- insufficient retrieved information

The application also uses logging to provide visibility into major pipeline stages such as:

```text
Query received
Embedding model loading
ChromaDB connection
Document retrieval
LLM generation
Answer generation
```

---

## Security and Configuration

Sensitive configuration such as the OpenAI API key is loaded through environment variables using `python-dotenv`.

The `.env` file is excluded from version control through `.gitignore`.

The project also excludes generated/runtime artifacts such as:

```text
.venv/
__pycache__/
chroma_db/
.vscode/
.env
```

---

## Limitations

This project is intended as a demonstration of an end-to-end RAG architecture.

Current limitations include:

- evaluation is based on a small manually curated dataset
- answer evaluation currently uses expected keyword matching
- the application primarily processes text extracted from PDF documents
- semantic retrieval may still return similar but irrelevant chunks for unsupported questions
- abstention behavior currently relies on the grounding instructions provided to the language model
- no production authentication or authorization layer is implemented
- no cloud deployment is included in the current version

---

## Future Improvements

Potential future improvements include:

- larger and more diverse evaluation datasets
- automated answer-quality evaluation
- retrieval relevance thresholds
- reranking models
- hybrid keyword + semantic retrieval
- conversational memory
- document upload through the UI
- improved multimodal document processing
- production deployment
- monitoring and observability
- evaluation dashboards

---

## Key Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation
- document ingestion
- document chunking
- semantic embeddings
- vector databases
- semantic search
- prompt engineering
- grounded LLM generation
- abstention handling
- retrieval evaluation
- end-to-end RAG evaluation
- source attribution
- Streamlit application development
- Python logging and error handling
- Git-based version control
