from app.ingestion.pdf_load import load_pdf
from app.ingestion.chunker import sentence_chunker
from app.embeddings.embedding_service import EmbeddingService
from app.vector_database.qdrant_manager import QdrantManager
import os
import pickle


embedding_service = EmbeddingService()
qdrant = QdrantManager()
qdrant.delete_collection()
qdrant.create_collection(vector_size=384)
DATA_FOLDER = "app/data"
pdf_files = [
    file
    for file in os.listdir(DATA_FOLDER)
    if file.lower().endswith(".pdf")
]

all_chunks=[]

for pdf_file in pdf_files:

    pdf_path = os.path.join(DATA_FOLDER, pdf_file)

    print(f"\nProcessing {pdf_file}")

    pages = load_pdf(pdf_path)

    chunks = sentence_chunker(pages)
    all_chunks.extend(chunks)

    embeddings = embedding_service.embed_documents(chunks)

    qdrant.upload_documents(
        embeddings,
        chunks
    )
    
os.makedirs("app/storage", exist_ok=True)

with open("app/storage/chunks.pkl", "wb") as file:
    pickle.dump(all_chunks, file)

print(f"\nSaved {len(all_chunks)} chunks to app/storage/chunks.pkl")