from pathlib import Path
import os

DB_DIR = Path(__file__).resolve().parents[2] / "data" / "vector_db"

def _collection():
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("ChromaDB is missing. Install requirements.txt.") from exc
    client = chromadb.PersistentClient(path=str(DB_DIR))
    return client.get_or_create_collection("codepilot_knowledge", metadata={"hnsw:space":"cosine"})

def add_chunks(ids, texts, embeddings, metadatas):
    _collection().upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)

def search(embedding, top_k=5):
    col = _collection()
    if col.count() == 0: return []
    result = col.query(query_embeddings=[embedding], n_results=min(top_k, col.count()))
    rows = []
    for i, doc in enumerate(result["documents"][0]):
        rows.append({"text":doc, "metadata":result["metadatas"][0][i], "distance":result["distances"][0][i]})
    return rows

def list_documents():
    col = _collection()
    data = col.get(include=["metadatas"])
    seen = {}
    for m in data.get("metadatas", []):
        seen[m.get("document_id")] = {"name":m.get("filename"), "chunks":seen.get(m.get("document_id"),{}).get("chunks",0)+1}
    return [{"id":k, **v} for k,v in seen.items()]

def delete_document(document_id):
    col = _collection()
    col.delete(where={"document_id":document_id})
