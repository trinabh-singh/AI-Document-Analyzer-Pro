import pickle
import string
import nltk
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download("punkt")
nltk.download('stopwords')
class BM25Retriever:
    def tokenize(self,text):
        tokens = word_tokenize(text.lower())

        return [
            token
            for token in tokens
            if token not in self.stop_words
            and token not in string.punctuation
        ]

    def __init__(
        self,
        chunk_file="app/storage/chunks.pkl"
    ):
        self.stop_words = set(stopwords.words("english"))
        with open(chunk_file, "rb") as file:
            self.chunks = pickle.load(file)

        self.corpus = [
            self.tokenize(chunk["content"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(self.corpus)



    

    def search(
        self,
        query,
        top_k=10
    ):

        tokenized_query = self.tokenize(query)
        
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indices:
            if scores[index] <= 0:
                continue
            chunk = self.chunks[index]

            results.append(
                {
                    "chunk": chunk["content"],
                    "score": float(scores[index]),
                    "metadata": {
                        "chunk_id": chunk["chunk_id"],
                        "page_number": chunk["page_number"],
                        "strategy": chunk["strategy"],
                        "document_id": chunk["document_id"],
                        "document_name": chunk["document_name"]
                    }
                }
            )

        return results