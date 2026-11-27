from pathlib import Path
import hashlib, json, re
from pypdf import PdfReader
from docx import Document

def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    if ext == ".docx":
        return "\n".join(p.text for p in Document(str(path)).paragraphs)
    if ext == ".txt" or ext == ".md":
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError("Supported formats: PDF, DOCX, TXT and MD.")

def chunk_text(text: str, size: int = 1100, overlap: int = 160):
    text = re.sub(r"\s+", " ", text).strip()
    if not text: return []
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start + size // 2, end)
            if boundary > start: end = boundary
        chunks.append(text[start:end].strip())
        if end >= len(text): break
        start = max(end - overlap, start + 1)
    return chunks

def document_id(name: str, content: str):
    return hashlib.sha256((name + content).encode("utf-8")).hexdigest()[:20]
