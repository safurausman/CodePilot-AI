import os
from google import genai
from google.genai import types

def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT"):
    key = os.getenv("GEMINI_API_KEY")
    if not key: raise RuntimeError("Set GEMINI_API_KEY before using RAG.")
    client = genai.Client(api_key=key)
    model = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
    vectors = []
    for text in texts:
        result = client.models.embed_content(
            model=model,
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        vectors.append(result.embeddings[0].values)
    return vectors
