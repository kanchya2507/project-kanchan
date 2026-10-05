import logging
from dataclasses import dataclass, field
from threading import Lock
from uuid import uuid4

from groq import Groq

from app.rag.config import GROQ_API_KEY, GROQ_MODEL
from app.rag.prompt import SYSTEM_PROMPT
from app.rag.store import search


@dataclass
class InterviewSession:
    source: str | None
    messages: list[dict[str, str]] = field(default_factory=list)
    last_question: str = ""


_sessions: dict[str, InterviewSession] = {}
_sessions_lock = Lock()
logger = logging.getLogger(__name__)


def _call_groq(messages: list[dict[str, str]]) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured in project-api/.env")

    try:
        response = Groq(api_key=GROQ_API_KEY).chat.completions.create(
            model=GROQ_MODEL,
            temperature=0.2,
            max_tokens=900,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],
        )
    except Exception as exc:
        logger.exception("Groq API request failed")
        raise RuntimeError(
            "The Groq request failed. Check the API key and configured model."
        ) from exc

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty response")
    return content.strip()


def _format_context(chunks: list[dict]) -> str:
    if not chunks:
        return "No matching PDF excerpts were found."

    return "\n\n".join(
        f"[Source: {item['metadata']['source']}, "
        f"page {item['metadata']['page']}]\n{item['text']}"
        for item in chunks
    )


def start_interview(source: str | None = None) -> tuple[str, str]:
    chunks = search(
        "DevOps technical topics, tools, responsibilities, processes, and concepts",
        source,
    )
    if not chunks:
        raise ValueError(
            "No indexed PDF excerpts found. Add a PDF and run ingestion first."
        )

    prompt = (
        "Start the interview. Ask exactly one technical question based only on "
        "these PDF excerpts. Do not give the answer or hints.\n\n"
        f"PDF excerpts:\n{_format_context(chunks)}"
    )
    question = _call_groq([{"role": "user", "content": prompt}])

    session_id = str(uuid4())
    session = InterviewSession(
        source=source,
        messages=[{"role": "assistant", "content": question}],
        last_question=question,
    )
    with _sessions_lock:
        _sessions[session_id] = session

    return session_id, question


def submit_answer(session_id: str, answer: str) -> str:
    with _sessions_lock:
        session = _sessions.get(session_id)

    if session is None:
        raise KeyError("Interview session not found; start a new interview.")

    chunks = search(
        f"{session.last_question}\nCandidate answer: {answer}",
        session.source,
    )
    prompt = (
        f"Previous interview question:\n{session.last_question}\n\n"
        f"Candidate answer:\n{answer}\n\n"
        f"Relevant PDF excerpts:\n{_format_context(chunks)}\n\n"
        "Evaluate the answer using the system instructions. Give feedback, an "
        "integer score from 1 to 10, improvement suggestions, and at most one "
        "next question."
    )

    # Bound stored history to keep requests from growing without limit.
    reply = _call_groq(
        [*session.messages[-10:], {"role": "user", "content": prompt}]
    )
    with _sessions_lock:
        session.messages.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": reply},
        ])
        session.messages = session.messages[-12:]
        session.last_question = reply

    return reply
