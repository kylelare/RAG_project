from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "chroma"
embeddings = HuggingFaceEmbeddings()


def main():
    save_documents()


def save_documents():
    documents = load_documents()
    save_to_chroma(documents)


def load_documents():
    loader = PyPDFLoader("pdfs/resume.pdf")
    documents = loader.load_and_split()
    return documents


def save_to_chroma(chunks: list[Document]):
    # Clear out old database first
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, HuggingFaceEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
