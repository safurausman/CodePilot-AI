# CodePilot AI

A multi-page Generative AI workspace built with Python, Gradio and Gemini.

## Features

- **AI Coding Workspace:** Generate, explain, debug, review, optimize code and write tests. Proposed code is previewed and saved only after approval.
- **Knowledge Hub (RAG):** Upload PDF, DOCX, TXT or Markdown files; extract and chunk text; create Gemini embeddings; persist vectors in ChromaDB; retrieve relevant chunks for grounded answers with source references.
- **Tools Center:** Restricted AST-based Python expression evaluator, generated-file listing/reading and a time-limited `unittest` runner.
- **AI Agent:** Gemini produces a bounded plan and selects from registered tools. Tool calls and their real execution results are shown. File creation is not performed without user approval.
- **Dashboard and Activity:** Real counts and SQLite-backed activity records.

## Requirements

- Python 3.10+
- Gemini API key with access to the selected text and embedding models.

## Setup (Windows PowerShell)

```powershell
cd E:\Projects\CodePilot_AI
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY`. The application reads `.env` automatically only if you add `python-dotenv` loading; alternatively set the environment variable in the terminal:

```powershell
$env:GEMINI_API_KEY="YOUR_REAL_KEY"
python app.py
```

Open http://127.0.0.1:7860

For Command Prompt:

```cmd
set GEMINI_API_KEY=YOUR_REAL_KEY
python app.py
```

## RAG workflow

1. Open Knowledge Hub.
2. Upload PDF, DOCX, TXT or MD documents (12 MB maximum per file).
3. Click Process & Index Documents.
4. Ask questions in the chat. Answers use retrieved chunks and cite source filenames/chunk numbers.
5. The persistent ChromaDB index is stored in `data/vector_db`; original uploaded documents are stored in `data/documents`.

## Tools and safety

- The Python evaluator supports a restricted expression grammar and safe math/list functions. It does not execute arbitrary Python scripts.
- File tools only read/list files inside `codepilot_outputs`.
- The test runner invokes `python -m unittest` on a selected `.py` module in `codepilot_outputs`, with a 20-second timeout. Only run trusted test files; tests are executable code.
- The AI Agent can plan and invoke registered tools. Its action count is capped. It cannot run shell commands or unrestricted Python. File creation is intentionally not automatic.
- This is a local development build, not a hardened multi-tenant production sandbox. Before public deployment, add authentication, per-user storage isolation, request quotas, upload malware scanning, and a dedicated OS/container sandbox for running tests.

## Existing project files

Previously generated calculator source files and the existing calculator test module are retained in `codepilot_outputs/`. The existing test module imports the calculator module by sibling filename; run it from that folder:

```powershell
cd codepilot_outputs
python -m unittest -v codepilot_generated_generate_code_optimize_code_write_tests_write_tests
```

## Project structure

```text
app.py
modules/
  rag/       document extraction, embeddings, vector store, retrieval
  tools/     restricted Python, file tools, unit-test runner
  agents/    bounded plan-and-execute agent
data/
  documents/
  vector_db/
codepilot_outputs/
tests/
requirements.txt
.env.example
codepilot_workspace.db
```

## Deployment notes

Set `GEMINI_API_KEY` as a hosting-provider secret. Use persistent volumes for `data/`, `codepilot_outputs/` and `codepilot_workspace.db`. Set `HOST=0.0.0.0` and configure `PORT` from the hosting platform. Do not expose this unauthenticated local-development build publicly until authentication, storage isolation and sandboxing have been added.
