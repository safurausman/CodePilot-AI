from .embeddings import embed_texts
from .vector_store import search

def retrieve(question, top_k=5):
    vector = embed_texts([question], task_type="RETRIEVAL_QUERY")[0]
    return search(vector, top_k=top_k)
