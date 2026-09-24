

### In order to make our code resuable
### Instead of keeping document loading logic inside document_loader.py only, we'll create a function.

## Imports

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader


def load_documents():

    loader = DirectoryLoader(
        "data/pdfs",
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(f"Total Documents Loaded: {len(documents)}")