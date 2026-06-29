from app.embeddings.embedding_service import EmbeddingService
from app.vector_database.qdrant_manager import QdrantManager

embedding_service = EmbeddingService()
qdrant = QdrantManager()

query="what are the skills present?"

query_embedding=embedding_service.embed_query(query)

results=qdrant.search(query_embedding.tolist(),limit=3)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print(f"Score: {result['score']:.4f}")
    print(f"Page: {result['metadata']['page_number']}")
    print(f"Chunk ID: {result['metadata']['chunk_id']}")
    print("-" * 60)
    print(result['chunk'])