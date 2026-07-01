from app.embeddings.embedding_service import EmbeddingService
from app.vector_database.qdrant_manager import QdrantManager
from app.retrieval.bm25_retriever import BM25Retriever


class HybridRetriever:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.qdrant = QdrantManager()

        self.bm25 = BM25Retriever()

    def search(
        self,
        question,
        dense_top_k=10,
        bm25_top_k=10
    ):

        query_embedding = self.embedding_service.embed_query(question)

        dense_results = self.qdrant.search(
            query_embedding.tolist(),
            limit=dense_top_k
        )

        bm25_results = self.bm25.search(
            question,
            top_k=bm25_top_k
        )

        rrf_scores = {}
        k = 60

        for rank, result in enumerate(dense_results, start=1):

            chunk_id = result["metadata"]["chunk_id"]

            rrf_score = 1 / (k + rank)

            if chunk_id not in rrf_scores:

                rrf_scores[chunk_id] = {
                    "result": result,
                    "rrf_score": rrf_score
                }

            else:

                rrf_scores[chunk_id]["rrf_score"] += rrf_score


        for rank, result in enumerate(bm25_results, start=1):

            chunk_id = (result["metadata"]["document_id"],result["metadata"]["chunk_id"])

            rrf_score = 1 / (k + rank)

            if chunk_id not in rrf_scores:

                rrf_scores[chunk_id] = {
                    "result": result,
                    "rrf_score": rrf_score
                }

            else:

                rrf_scores[chunk_id]["rrf_score"] += rrf_score


        sorted_results = sorted(

            rrf_scores.values(),

            key=lambda item: item["rrf_score"],

            reverse=True
        )

        return [
            item["result"]
            for item in sorted_results
        ]