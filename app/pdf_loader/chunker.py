def fixed_size_chunker(
    documents: list[dict],
    chunk_size: int = 512,
    overlap: int = 50,
):
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
