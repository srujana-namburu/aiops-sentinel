from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def get_retriever():
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db.as_retriever()

def retrieve_context(query):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in docs])