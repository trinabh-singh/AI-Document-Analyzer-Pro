from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import RAGPipeline

app = FastAPI()

rag = RAGPipeline()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/query")
def query(request: QueryRequest):
    result = rag.ask(request.question)
    return result 