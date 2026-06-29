from app.retrieval.reranker import Reranker

reranker = Reranker()

question = "Who is Trinabh?"

chunks = [
    {"chunk": "Trinabh is an AI engineer."},
    {"chunk": "Paneer Butter Masala costs 270."},
    {"chunk": "Trinabh knows Python and Machine Learning."}
]

results = reranker.rerank(question, chunks, top_k=2)

for chunk in results:
    print(chunk["rerank_score"])
    print(chunk["chunk"])
    print("-" * 40)