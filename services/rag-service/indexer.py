import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

RUNBOOK_DIR = "runbooks"

def load_documents():
    docs = []
    for file in os.listdir(RUNBOOK_DIR):
        loader = TextLoader(os.path.join(RUNBOOK_DIR, file))
        docs.extend(loader.load())
    return docs

def create_index():
    docs = load_documents()

    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    texts = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    db.save_local("faiss_index")
    print("✅ Index created")

if __name__ == "__main__":
    create_index()