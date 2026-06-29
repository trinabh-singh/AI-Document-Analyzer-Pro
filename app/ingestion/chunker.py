from sklearn.metrics.pairwise import cosine_similarity
from nltk import tokenize
import nltk
nltk.download('punkt')
nltk.download("punkt_tab")

def fixed_size_chunker(
    documents: list[dict],
    chunk_size: int = 512,
    overlap: int = 50,
)-> list[dict]:
    chunks=[]
    chunk_id=1

    if overlap>=chunk_size:
        raise ValueError("Overlap cannot be greater than chunk Size")
        
    for doc in documents:

        c=doc["content"].split() 
        total_words=len(c)
        start=0
        l=[]
        
        while start<total_words:
            l=c[start:start+chunk_size] 
            chunks.append(
                {
                    "chunk_id":chunk_id,
                    "page_number": doc["page_number"],
                    "strategy":"fixed",
                    "content": " ".join(l)
                }
            )
            chunk_id+=1
            start+=chunk_size-overlap
    
    return chunks


def sentence_chunker(
    documents: list[dict],
    chunk_size: int = 512,
)-> list[dict]:
    chunks=[]
    chunk_id=1
     
    for doc in documents:

        c=nltk.sent_tokenize(doc["content"])
        
        current_chunk=[]
        length=0
        
       
        for i in c:
            current_len=len(i.split())
            
            if length+current_len>chunk_size:           
                if current_chunk:

                    chunks.append(
                        {
                            "chunk_id": chunk_id,
                            "document_id": doc["document_id"],
                            "document_name": doc["document_name"],
                            "page_number": doc["page_number"],
                            "strategy": "sentence",
                            "content": " ".join(current_chunk)
                        }
                    )
                    chunk_id+=1
                current_chunk=[]
                length=0
            

            current_chunk.append(i)
            length+=current_len
        
        
        chunks.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": doc["document_id"],
                    "document_name": doc["document_name"],
                    "page_number": doc["page_number"],
                    "strategy": "sentence",
                    "content": " ".join(current_chunk)
                }
                )
        chunk_id+=1
    
    return chunks


def semantic_chunker(
    documents,
    embedding_model,
    similarity_threshold=0.8,
)-> list[dict]:
    chunks=[]
    chunk_id=1

    for doc in documents:

        sentences=nltk.sent_tokenize(doc["content"])

        embeddings=embedding_model.encode(sentences)
        current_chunk=[]
        if current_chunk:
            current_chunk=[sentences[0]]

        for i in range(len(embeddings) - 1):
            similarity = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]

            if similarity>=similarity_threshold:
                current_chunk.append(sentences[i+1])
            else:
                chunks.append(
                        {
                            "chunk_id": chunk_id,
                            "document_id": doc["document_id"],
                            "document_name": doc["document_name"],
                            "page_number": doc["page_number"],
                            "strategy": "sentence",
                            "content": " ".join(current_chunk)
                        }
                    )
                chunk_id+=1
                current_chunk=[sentences[i+1]]

        if current_chunk:
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": doc["document_id"],
                    "document_name": doc["document_name"],
                    "page_number": doc["page_number"],
                    "strategy": "sentence",
                    "content": " ".join(current_chunk)
                }
                )
            chunk_id+=1
        

