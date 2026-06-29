class PromptBuilder:

    def build_prompt(self, question, retrieved_chunks):

        content = "\n\n".join(
            chunk["chunk"] for chunk in retrieved_chunks
        )

        prompt = f"""
You are an experienced AI assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. If the answer cannot be found in the context, reply:
   "I cannot find that information in the document."
3. Keep the answer clear, accurate, and concise.

Context:
{content}

Question:
{question}

Answer:
"""

        return prompt