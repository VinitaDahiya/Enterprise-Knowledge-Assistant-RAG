


'''

## Create Loader

loader=DirectoryLoader(
    "data/pdfs",          # go inside data->pdfs and search there
    glob="*.pdf",         #load every file ending with .pdf
    loader_cls=PyPDFLoader #This tells DirectoryLoader:Whenever you find a PDF,use PyPDFLoader to open it
    
)


## Load the Documents

documents = loader.load()


## Verify

print(f"Total Documents Loaded: {len(documents)}")


print("\n----------------------------")
print("First Document Object")
print("----------------------------")

print(documents[0])


## documents is not a single document, it is a list
print(type(documents))    #result: <class 'list'>


## specific documents type would be document object
print(type(documents[0]))  # result: <class 'langchain_core.documents.base.Document'>


## also check
print(documents[0].page_content)


print(documents[0].metadata)

'''


###
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