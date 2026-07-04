from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import Annotated
import os
import shutil
from app.ingestion.ingestion_pipeline import ingest_documents

from app.rag_pipeline import RAGPipeline

app = FastAPI()

rag=None

class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG API Running"}

UPLOAD_FOLDER = "app/data"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_pdfs(files: Annotated[list[UploadFile], File(...)]):
    global rag
    uploaded = []
    pdf_paths=[]

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded.append(file.filename)
        pdf_paths.append(file_path)
    total_chunks = ingest_documents(pdf_paths)
    rag = RAGPipeline()
    

    return {
        "message": "Files uploaded and indexed successfully",
        "files": uploaded,
        "chunks_created": total_chunks
    }

@app.post("/query")
def query(request: QueryRequest):

    global rag

    if rag is None:
        return {
            "error": "Please upload documents first."
        }

    try:
        result = rag.ask(request.question)
        return result

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {
            "error": str(e),
            "type": type(e).__name__
        }
