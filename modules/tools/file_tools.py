from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "codepilot_outputs"
OUTPUT.mkdir(exist_ok=True)

def list_output_files():
    return [p.name for p in OUTPUT.iterdir() if p.is_file()]

def read_output_file(filename):
    path=(OUTPUT / Path(filename).name).resolve()
    if path.parent != OUTPUT.resolve() or not path.is_file(): raise ValueError("File not found in output folder.")
    if path.stat().st_size > 200_000: raise ValueError("File is larger than 200 KB.")
    return path.read_text(encoding="utf-8",errors="replace")

def write_output_file(filename, content):
    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",Path(filename).name)
    if not safe or safe in {".",".."}: raise ValueError("Invalid filename.")
    if len(content)>100_000: raise ValueError("Content is limited to 100 KB.")
    path=OUTPUT/safe
    if path.exists(): raise FileExistsError("That filename already exists. Choose a new name.")
    path.write_text(content,encoding="utf-8")
    return str(path)
