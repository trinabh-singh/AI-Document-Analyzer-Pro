from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        question,
        retrieved_chunks,
        top_k=5
    ):

        pairs = [
            (question, chunk["chunk"])
            for chunk in retrieved_chunks
        ]

        scores = self.model.predict(pairs)

        for chunk, score in zip(retrieved_chunks, scores):
            chunk["rerank_score"] = float(score)

        reranked_chunks = sorted(
            retrieved_chunks,
            key=lambda chunk: chunk["rerank_score"],
            reverse=True
        )

        return reranked_chunks[:top_k]