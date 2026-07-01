from app.ingestion.pdf_load import load_pdf
from app.ingestion.chunker import sentence_chunker
from app.embeddings.embedding_service import EmbeddingService
from app.vector_database.qdrant_manager import QdrantManager
import os
import pickle


def ingest_documents(pdf_files):

    embedding_service = EmbeddingService()
    qdrant = QdrantManager()

    # Rebuild the collection
    qdrant.delete_collection()
    qdrant.create_collection(vector_size=384)

    all_chunks = []

    for pdf_path in pdf_files:

        print(f"\nProcessing {os.path.basename(pdf_path)}")

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

    print(f"\nSaved {len(all_chunks)} chunks.")

    return len(all_chunks)


if __name__ == "__main__":

    DATA_FOLDER = "app/data"

    pdf_files = [
        os.path.join(DATA_FOLDER, file)
        for file in os.listdir(DATA_FOLDER)
        if file.lower().endswith(".pdf")
    ]

    ingest_documents(pdf_files)