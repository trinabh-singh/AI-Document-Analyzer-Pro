from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        print("API Key:", os.getenv("OPENROUTER_API_KEY"))

    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model="GPT-OSS-120B",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print("\n===== LLM RESPONSE =====")
        print(response)
        print("========================\n")

        if response.choices is None:
            raise Exception(f"Model returned no choices:\n{response}")

        if len(response.choices) == 0:
            raise Exception("Model returned an empty choices list.")

        print(response.model_dump())

        return response.choices[0].message.content