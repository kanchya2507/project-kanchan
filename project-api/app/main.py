import html
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.rag.routes import router as interview_router

APP_VERSION = os.getenv("APP_VERSION", "3.0.0")
BUILD_SHA = os.getenv("BUILD_SHA", "local/dev")

app = FastAPI(
    title="DevOps Knowledge Agent",
    description="DevOps Q&A powered by your indexed PDF knowledge base. Swagger is available for the QA API.",
    version=APP_VERSION,
    openapi_tags=[
        {
            "name": "QA Console",
            "description": "Ask DevOps questions and get answers grounded in your indexed PDF knowledge base.",
        },
        {
            "name": "System",
            "description": "Swagger and runtime access information.",
        },
    ],
)

app.include_router(
    interview_router,
    prefix="/api/interview",
    tags=["DevOps interviewer"],
)

@app.get("/health", tags=["System"], summary="Check application health")
def health_check():
  return {"status": "ok"}


@app.get("/", response_class=HTMLResponse, tags=["QA Console"], summary="Open DevOps QA landing page")
def root_dashboard():
    page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DevOps Knowledge Agent</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4efe4;
      --panel: #fffdf8;
      --text: #202d27;
      --muted: #68736b;
      --line: #e3dccd;
      --gold: #e3a92f;
      --coral: #c95d3c;
      --forest: #31594b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: linear-gradient(135deg, #f7f1e5 0%, #f1eadb 58%, #e9eee5 100%);
      color: var(--text);
      font-family: Inter, Segoe UI, sans-serif;
    }
    .card {
      width: min(760px, calc(100% - 32px));
      background: var(--panel);
      border: 1px solid #e7decc;
      border-radius: 8px;
      padding: 36px 28px;
      box-shadow: 0 24px 70px rgba(54, 48, 33, .10);
    }
    .eyebrow { color: var(--coral); font-size: 12px; letter-spacing: .15em; text-transform: uppercase; font-weight: 800; }
    h1 { margin: 12px 0 10px; font-size: clamp(30px, 4vw, 48px); }
    p { color: var(--muted); line-height: 1.7; }
    .intro { max-width: 620px; font-size: 17px; }
    .details { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 28px; }
    .detail { border-top: 1px solid var(--line); padding-top: 14px; }
    .detail strong { display: block; margin-bottom: 6px; }
    .detail p { margin: 0; font-size: 14px; }
    .note { margin-top: 22px; padding: 12px 14px; border-left: 3px solid var(--gold); background: #fbf4e4; font-size: 14px; }
    .actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 22px; }
    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 18px;
      border-radius: 12px;
      text-decoration: none;
      font-weight: 700;
      border: 1px solid var(--line);
      color: var(--text);
      background: #fffdf8;
    }
    .button.primary {
      background: var(--forest);
      color: #fffdf8;
      border: 0;
    }
    .button:hover { border-color: var(--coral); }
    @media (max-width: 620px) {
      .card { padding: 28px 20px; }
      .details { grid-template-columns: 1fr; gap: 14px; }
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="eyebrow">DevOps Knowledge Agent</div>
    <h1>Your DevOps documents, ready for questions.</h1>
    <p class="intro">Ask about the tools, processes, and guidance covered in your indexed PDF files. The agent finds relevant passages and uses them to shape a direct answer.</p>
    <div class="details">
      <div class="detail">
        <strong>Ask naturally</strong>
        <p>Type a question about DevOps, cloud platforms, CI/CD, or topics covered by your documents.</p>
      </div>
      <div class="detail">
        <strong>Answers from your PDFs</strong>
        <p>The agent looks for relevant information in the indexed PDF knowledge base.</p>
      </div>
      <div class="detail">
        <strong>Know what’s covered</strong>
        <p>If the documents don’t contain enough information, the agent will tell you instead of guessing.</p>
      </div>
    </div>
    <p class="note">Answers are based on your indexed documents, not general web search. Add and index relevant PDFs to expand what the agent can answer.</p>
    <div class="actions">
      <a class="button primary" href="/qa">Ask a question</a>
      <a class="button" href="/docs">Swagger</a>
    </div>
  </div>
</body>
</html>
"""
    return HTMLResponse(page)


@app.get("/qa", response_class=HTMLResponse, tags=["QA Console"], summary="Open DevOps Q&A panel")
def qa_dashboard():
    page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Interview Q&A Panel</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4efe4;
      --panel: #fffdf8;
      --panel-light: #f8f3e9;
      --text: #202d27;
      --muted: #68736b;
      --line: #e3dccd;
      --gold: #e3a92f;
      --coral: #c95d3c;
      --forest: #31594b;
      --green: #347251;
      --danger: #b43d31;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, Segoe UI, sans-serif;
      background: linear-gradient(135deg, #f7f1e5 0%, #f1eadb 58%, #e9eee5 100%);
      color: var(--text);
      min-height: 100vh;
    }
    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 60px;
    }
    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 28px;
    }
    .nav a {
      color: var(--muted);
      text-decoration: none;
      margin-left: 16px;
    }
    .card {
      background: var(--panel);
      border: 1px solid #e7decc;
      border-radius: 8px;
      box-shadow: 0 18px 45px rgba(54, 48, 33, .08);
      padding: 24px;
      margin-bottom: 20px;
    }
    h1 { margin: 0 0 8px; font-size: clamp(30px, 4vw, 44px); }
    .subtitle { color: var(--muted); margin: 0 0 18px; }
    .grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 20px;
    }
    label {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 13px;
      letter-spacing: .04em;
      text-transform: uppercase;
    }
    input, textarea, button {
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #fffefa;
      color: var(--text);
      font: inherit;
    }
    input, textarea {
      padding: 12px 14px;
    }
    textarea {
      min-height: 160px;
      resize: vertical;
    }
    button {
      cursor: pointer;
      padding: 12px 16px;
      font-weight: 700;
      transition: background-color .2s ease, border-color .2s ease, transform .2s ease;
    }
    button.primary {
      background: var(--forest);
      color: #fffdf8;
      border: 0;
    }
    button.secondary {
      background: #fbf1dc;
      border-color: #ead6aa;
      color: #765018;
    }
    button:hover { transform: translateY(-1px); }
    button.primary:hover { background: #244738; }
    .status-box {
      border: 1px solid #e8d7ac;
      background: #fbf4e4;
      border-radius: 8px;
      padding: 16px;
      margin-top: 14px;
    }
    .muted { color: var(--muted); }
    .question {
      font-size: 1.08rem;
      line-height: 1.6;
      white-space: pre-wrap;
    }
    .result {
      white-space: pre-wrap;
      line-height: 1.7;
      color: var(--forest);
    }
    .result p { margin: 0 0 12px; }
    .result ul { margin: 0 0 14px; padding-left: 22px; }
    .result strong { color: var(--coral); }
    .result h2, .result h3 { margin: 4px 0 10px; color: var(--text); }
    .error { color: var(--danger); }
    @media (max-width: 850px) {
      .grid { grid-template-columns: 1fr; }
      .topbar { flex-direction: column; align-items: flex-start; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div>
        <div class="muted">Agent training / interview</div>
      </div>
      <div class="nav">
        <a href="/">Dashboard</a>
        <a href="/docs">Swagger</a>
      </div>
    </div>

    <div class="card">
      <h1>DevOps Q&A</h1>
      <p class="subtitle">Ask a DevOps question and get an answer based on your indexed PDF content.</p>
      <div class="grid">
        <div>
          <label for="pdf-file">Optional PDF file</label>
          <input id="pdf-file" type="text" placeholder="example: devops-notes.pdf" />
        </div>

        <div>
          <label for="question-box">Your question</label>
          <textarea id="question-box" placeholder="Ask anything related to DevOps, CI/CD, Docker, Kubernetes, AWS, monitoring, etc..."></textarea>
          <div style="margin-top: 16px; display: flex; gap: 12px;">
            <button id="ask-btn" class="primary" type="button">Ask agent</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="muted">Answer</div>
      <div id="result" class="result">Ask a question to get an answer.</div>
    </div>
  </div>

  <script>
    const questionEl = document.getElementById('question-box');
    const resultEl = document.getElementById('result');
    const pdfInput = document.getElementById('pdf-file');

    function renderMarkdown(markdown) {
      const escapeHTML = value => value.replace(/[&<>"']/g, character => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      })[character]);
      const formatInline = value => escapeHTML(value)
        .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');

      let output = '';
      let inList = false;
      const closeList = () => {
        if (inList) output += '</ul>';
        inList = false;
      };

      for (const line of markdown.split(/\\r?\\n/)) {
        const trimmed = line.trim();
        const item = trimmed.match(/^[-*]\\s+(.+)/);
        const heading = trimmed.match(/^(#{1,3})\\s+(.+)/);

        if (!trimmed) {
          closeList();
        } else if (item) {
          if (!inList) output += '<ul>';
          inList = true;
          output += `<li>${formatInline(item[1])}</li>`;
        } else {
          closeList();
          if (heading) {
            const level = Math.min(heading[1].length + 1, 3);
            output += `<h${level}>${formatInline(heading[2])}</h${level}>`;
          } else {
            output += `<p>${formatInline(trimmed)}</p>`;
          }
        }
      }

      closeList();
      return output;
    }

    async function askQuestion() {
      const question = questionEl.value.trim();
      if (!question) {
        resultEl.textContent = 'Please enter a question before submitting.';
        resultEl.classList.add('error');
        return;
      }

      resultEl.textContent = 'Thinking...';
      resultEl.classList.remove('error');

      try {
        const response = await fetch('/api/interview/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: question,
            document: pdfInput.value.trim() || null,
          }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Unable to answer question');
        }

        let answer = data.answer || '';
        answer = answer.replace(/^\\s*Question\\s*:\\s*/i, '');
        resultEl.innerHTML = renderMarkdown(answer);
      } catch (error) {
        resultEl.textContent = error.message;
        resultEl.classList.add('error');
      }
    }

    const askButton = document.getElementById('ask-btn');
    askButton.addEventListener('click', askQuestion);

    questionEl.addEventListener('keydown', function (event) {
      if ((event.key === 'Enter' || event.keyCode === 13) && !event.shiftKey && !event.isComposing) {
        event.preventDefault();
        askButton.click();
      }
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(page)


