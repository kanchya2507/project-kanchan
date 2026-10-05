# DevOps Interviewer (RAG)

This feature adds a PDF-grounded interview API to the existing FastAPI app.
PDF text is split into chunks, embedded locally with Sentence Transformers, and
stored in Chroma. Relevant excerpts are sent to Groq to generate questions and
evaluate answers.

## Setup (Windows PowerShell)

From the `project-api` directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your `GROQ_API_KEY`. Keep the real key private and never
commit `.env`.

## Add and index PDFs

Copy study PDFs into `project-api/data/pdfs/`, then from `project-api` run:

```powershell
New-Item -ItemType Directory -Force data\pdfs
python -m app.rag.ingest
```

To index one PDF by filename:

```powershell
python -m app.rag.ingest --file devops-notes.pdf
```

The first ingestion downloads the configured sentence-transformer embedding
model. The PDF is chunked and embedded locally; the Groq API key is only used
when chatting.

## Run and use the API

From `project-api`:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

1. Call `POST /api/interview/start` with `{"document":"devops-notes.pdf"}`.
   Omit `document` to search all indexed PDFs.
2. Copy the returned `session_id` and question.
3. Call `POST /api/interview/{session_id}/answer` with
   `{"answer":"Your answer here"}`.

## Security and deployment notes

- `.env`, PDFs, and the generated Chroma database are excluded by
  `project-api/.gitignore`.
- Retrieved PDF excerpts are sent to Groq. Only use documents you are permitted
  and comfortable sending to that service.
- Interview sessions currently live in process memory and are lost on restart;
  this implementation is for local development/single-process use.
- A local Chroma database inside an ECS container may disappear when that task
  is replaced. Use durable storage or rebuild the index from durable PDF storage
  before relying on it in production.
- For ECS, inject `GROQ_API_KEY` at runtime from AWS Secrets Manager; do not bake
  it into the Docker image or commit it.
