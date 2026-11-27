# CodePilot AI Architecture

```mermaid
flowchart TD
  U[User] --> UI[Gradio Multi-page UI]
  UI --> CW[AI Coding Workspace]
  UI --> KH[Knowledge Hub]
  UI --> TC[Tools Center]
  UI --> AG[AI Agent]
  CW --> GM[Gemini LLM API]
  KH --> DP[PDF/DOCX/TXT Extraction]
  DP --> CH[Chunking]
  CH --> EM[Gemini Embeddings]
  EM --> VS[(Persistent ChromaDB)]
  KH --> RT[Semantic Retrieval]
  RT --> VS
  RT --> GM
  AG --> GM
  GM --> TP[Tool Planner]
  TP --> REG[Registered Tool Registry]
  REG --> PY[Restricted AST Evaluator]
  REG --> FT[Workspace File Tools]
  REG --> UT[Timed unittest Runner]
  UI --> DB[(SQLite Activity History)]
```

## Main flows

- Coding: user prompt/file → prompt builder → Gemini → conversation and proposed code → explicit approval → new output file.
- RAG: upload → extract → chunk → embed → ChromaDB → query embedding → top-k retrieval → Gemini grounded answer with source labels.
- Agent: user goal → Gemini JSON plan → allowlisted tool invocation → captured results → Gemini final synthesis.
