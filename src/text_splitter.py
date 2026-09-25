
## imports

from langchain_text_splitters import RecursiveCharacterTextSplitter   #This class will split our documents into smaller chunks.
from src.document_loader import load_documents



def create_chunks():
    documents = load_documents()    #Load documents and split them into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(         ## Create the Text Splitter 
        chunk_size=1000,
        chunk_overlap=200
    )




    ## Split the Documents

    chunks = text_splitter.split_documents(documents)
    return chunks
 
 
