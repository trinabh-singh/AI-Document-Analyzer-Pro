from app.vector_database.qdrant_manager import QdrantManager
from app.generation.prompt import PromptBuilder
from app.generation.llm_service import LLMService
from app.retrieval.reranker import Reranker
from app.retrieval.hybrid_retriever import  HybridRetriever
class RAGPipeline:

    def __init__(self):

        self.hybrid_retriever = HybridRetriever()

        self.qdrant = QdrantManager()

        self.prompt_builder = PromptBuilder()

        self.llm = LLMService()

        self.top_k=10

        self.reranker = Reranker()
    
    def ask(self, question):


        retrieved_chunks = self.hybrid_retriever.search(question,dense_top_k=self.top_k,bm25_top_k=self.top_k)

        reranked_chunks = self.reranker.rerank(question,retrieved_chunks,top_k=5)
        print("\nAfter Hybrid Retrieval\n")
        for chunk in retrieved_chunks:
            print(chunk["metadata"]["document_name"])
            print(chunk["metadata"]["chunk_id"])

        print("\nAfter Reranking\n")

        for i, chunk in enumerate(reranked_chunks, start=1):

            print(f"{i}. Score: {chunk['rerank_score']:.2f}")

            print(chunk["metadata"]["document_name"])

            print("-" * 40)

        prompt = self.prompt_builder.build_prompt(question,reranked_chunks)

        answer = self.llm.generate(prompt)
        

        return {
                "answer": answer,
                "chunks": reranked_chunks 
                }
    
if __name__ == "__main__":

    rag = RAGPipeline()

    question = input("Question:  ")

    answer = rag.ask(question)


    
    print("\nAnswer:\n")
    print(answer["answer"])

    print("\nSources\n")

    for chunk in answer["chunks"]:
        print(
            f"{chunk['metadata']['document_name']} "
            f"(Page {chunk['metadata']['page_number']})"
        )

