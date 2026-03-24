from fastapi import FastAPI
from retriever import retrieve_context

app = FastAPI()

@app.get("/retrieve")
def retrieve(query: str):
    context = retrieve_context(query)
    return {"context": context}