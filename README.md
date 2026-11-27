# CodePilot AI

**An AI-powered software development workspace built with Python, Gradio, and Google Gemini.**

CodePilot AI is a multi-page Generative AI application designed to assist developers throughout the software development lifecycle. It combines AI-powered coding assistance, Retrieval-Augmented Generation (RAG), restricted development tools, and an AI agent in one workspace.

## Features

### 1. Dashboard
- Provides an overview of the application.
- Displays project activity and workspace statistics.
- Gives users access to the main application modules.

### 2. AI Coding Workspace
- Generate code from natural-language prompts.
- Explain existing code.
- Debug and identify potential issues.
- Review code for quality and improvements.
- Optimize existing implementations.
- Generate unit tests.
- Preview proposed code before approving and saving it.

### 3. Knowledge Hub – RAG
- Upload PDF, DOCX, TXT, and Markdown documents.
- Extract and split document content into smaller chunks.
- Generate embeddings using Google Gemini.
- Store document vectors in ChromaDB.
- Retrieve relevant information using semantic search.
- Generate grounded answers using retrieved document context.
- Display source filenames and chunk references with answers.

### 4. Tools Center
- Execute restricted Python expressions using an AST-based evaluator.
- List and read generated files.
- Run Python unit tests using the built-in test runner.
- Apply execution time limits to test runs.

### 5. AI Agent
- Generate an execution plan based on user instructions.
- Select and invoke registered tools.
- Display tool calls and their actual execution results.
- Restrict the number of agent actions.
- Require user approval before creating files.

### 6. Activity & History
- Record application activities.
- Maintain activity history using SQLite.
- Provide visibility into previous workspace operations.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Gradio |
| Large Language Model | Google Gemini |
| Embeddings | Gemini Embedding Model |
| Vector Database | ChromaDB |
| Activity Storage | SQLite |
| Document Processing | PDF, DOCX, TXT, Markdown |
| Testing | Python unittest |
| Code Evaluation | Restricted AST-based evaluator |

## Application Architecture

The application is organized into separate modules to keep the coding workspace, RAG functionality, tools, and agent logic independent.

```text
CodePilot-AI/
│
├── app.py
│
├── modules/
│   ├── agents/
│   │   └── agent.py
│   │
│   ├── rag/
│   │   ├── document_processor.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   └── vector_store.py
│   │
│   └── tools/
│       ├── file_tools.py
│       ├── safe_python.py
│       └── test_runner.py
│
├── tests/
│   ├── README.md
│   └── test_safe_python_tool.py
│
├── codepilot_outputs/
│
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── README.md
└── requirements.txt
```

Runtime data such as uploaded documents, vector database files, and the SQLite workspace database are created or populated locally when the application runs. These files are not included in the source repository.

## Requirements

- Python 3.10 or later.
- Google Gemini API key with access to the configured text and embedding models.
- Internet connection for Gemini API requests.

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/safurausman/CodePilot-AI.git
cd CodePilot-AI
```

### 2. Create a virtual environment

```powershell
py -3.11 -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Set your API key as an environment variable:

```powershell
$env:GEMINI_API_KEY="YOUR_REAL_API_KEY"
```

Replace `YOUR_REAL_API_KEY` with your own Gemini API key. Never commit your actual API key to GitHub.

### 6. Run the application

```powershell
python app.py
```

Open the application in your browser:

**http://127.0.0.1:7860**

## Using the Application

### AI Coding Workspace
1. Open the AI Coding Workspace tab.
2. Select the required coding operation.
3. Enter a prompt or provide source code.
4. Generate the response.
5. Review the generated result.
6. Approve and save the code when appropriate.

### Knowledge Hub – RAG
1. Open the Knowledge Hub tab.
2. Upload a supported document.
3. Click **Process & Index Documents**.
4. Wait for document processing and indexing.
5. Ask a question related to the uploaded content.
6. Review the generated answer and its source references.

Supported document formats include PDF, DOCX, TXT, and Markdown. The application enforces a 12 MB maximum per file.

### Tools Center
1. Open Tools Center.
2. Use the restricted Python evaluator for supported expressions.
3. Refresh the generated-file list.
4. Read generated files.
5. Select a trusted test module and execute the unit tests.

### AI Agent
1. Open the AI Agent tab.
2. Enter a task in natural language.
3. Review the generated execution plan.
4. Allow the agent to select and execute registered tools.
5. Review the actual tool results and final response.

## Security and Safety Considerations

CodePilot AI includes safeguards for its development tools:

- The Python evaluator accepts a restricted expression grammar instead of executing arbitrary Python scripts.
- File tools are restricted to the `codepilot_outputs` directory.
- The unit-test runner uses a 20-second execution timeout.
- Test files contain executable code and should only be run when trusted.
- The AI Agent can only invoke registered tools and has a bounded action count.
- File creation requires user approval.

**Deployment warning:** This project is intended as a local development application and is not a hardened multi-user production environment. Before public deployment, implement authentication, per-user storage isolation, request quotas, upload scanning, and dedicated OS/container-level sandboxing for executable tests.

## Testing

The project includes automated tests for the restricted Python evaluator and additional testing capabilities through Tools Center.

To run the existing safe Python tool tests:

```powershell
python -m unittest discover -s tests -v
```

The Tools Center also provides a unit-test runner for selected generated test modules.

## Environment Configuration

The application uses the following environment variable:

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key used for Google Gemini integration |

An `.env.example` file is included as a configuration reference. Do not upload real credentials or secrets.

## Future Improvements

Potential future enhancements include:

- User authentication and access management.
- Multi-user workspace support.
- Enhanced agent planning and tool orchestration.
- Improved document management and retrieval.
- Production-grade execution sandboxing.
- Cloud deployment with persistent storage.

## Project Information

**Project:** CodePilot AI  
**Module:** Codomax Module 06  
**Repository:** [CodePilot-AI](https://github.com/safurausman/CodePilot-AI)

---

*CodePilot AI demonstrates the integration of Large Language Models, Prompt Engineering, Retrieval-Augmented Generation, development tools, and AI agents into a unified software development workspace.*
