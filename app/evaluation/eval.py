import json

from app.generation.llm_service import LLMService


class RAGASEvaluator:

    def __init__(self):
        self.llm = LLMService()

    def evaluate(self, question, answer, contexts):

        context_text = "\n\n".join(contexts)

        prompt = f"""
You are an expert evaluator for Retrieval-Augmented Generation (RAG).

Question:
{question}

Retrieved Context:
{context_text}

Generated Answer:
{answer}

Evaluate the answer using ONLY the retrieved context.

Score the following metrics from 0.0 to 1.0.

Faithfulness:
- Is every statement supported by the retrieved context?

Answer Relevancy:
- Does the answer directly answer the question?

Context Precision:
- Are the retrieved chunks relevant?

Context Recall:
- Did the retrieved chunks contain enough information to answer the question?

Return ONLY valid JSON.

Example:

{{
    "faithfulness":0.94,
    "answer_relevancy":0.91,
    "context_precision":0.88,
    "context_recall":0.93
}}
"""

        try:

            result = self.llm.generate(prompt)

            print("\n========== RAW EVALUATION ==========")
            print(result)
            print("====================================\n")

            result = result.replace("```json", "")
            result = result.replace("```", "").strip()

            scores = json.loads(result)

            return scores

        except Exception as e:

            print(e)

            return {
                "faithfulness":0,
                "answer_relevancy":0,
                "context_precision":0,
                "context_recall":0
            }