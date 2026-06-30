from app.retrieval.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()

results = retriever.search(
    "What are the skills?"
)


print("Dense Results:", len(dense_results))
print("BM25 Results :", len(bm25_results))
print("Hybrid Results:", len(combined_results))
for result in results:

    print(result["metadata"]["document_name"])
    print(result["metadata"]["chunk_id"])
    print("-" * 50)