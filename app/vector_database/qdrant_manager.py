from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
import uuid

class QdrantManager:

    def __init__(
        self,
        host="localhost",
        port=6333,
        collection_name="documents"
    ):
        self.client = QdrantClient(
            host=host,
            port=port,
            timeout=60
        )

        self.collection_name = collection_name

    def create_collection(self, vector_size: int = 384):
    
        if self.client.collection_exists(collection_name=self.collection_name):
            print(f"Collection '{self.collection_name}' already exists. Skipping creation.")
            return

    
        print(f"Creating collection '{self.collection_name}'...")
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size, 
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{self.collection_name}' created successfully.")

    def upload_documents(self, embeddings, chunks):
        
        points = []
        
        
        for chunk, embedding in zip(chunks, embeddings):
            
            point_id = str(uuid.uuid4())
            
            
            point = PointStruct(
                id=point_id,
                vector=embedding.tolist(),
                payload={
                    "text": chunk["content"],
                    "chunk_id": chunk["chunk_id"],
                    "page_number": chunk["page_number"],
                    "strategy": chunk["strategy"],
                    "document_id": chunk["document_id"],
                    "document_name": chunk["document_name"]
                }
            )
            points.append(point)
            
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_embedding: list, limit: int = 5):

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,          # <-- NOT query_vector
            limit=limit,
            with_payload=True
        )

        formatted_results = []

        for hit in response.points:

            payload = hit.payload if hit.payload else {}

            formatted_results.append(
                {
                    "chunk": payload.get("text", ""),
                    "score": hit.score,
                    "metadata": {k: v for k, v in payload.items() if k != "text"}
                }
            )

        return formatted_results
    
    def delete_collection(self):
        self.client.delete_collection(
            collection_name=self.collection_name
        )