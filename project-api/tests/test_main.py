from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_qa_endpoint_returns_answer(monkeypatch):
    def fake_answer_question(question, source=None):
        assert question == "What is CI/CD?"
        assert source is None
        return "CI/CD is the practice of automating build, test, and deployment workflows."

    monkeypatch.setattr("app.rag.routes.answer_question", fake_answer_question)

    response = client.post(
        "/api/interview/ask",
        json={"question": "What is CI/CD?"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "CI/CD is the practice of automating build, test, and deployment workflows."


def test_qa_endpoint_requires_question():
    response = client.post(
        "/api/interview/ask",
        json={},
    )

    assert response.status_code == 422


def test_qa_endpoint_rejects_path_traversal_document():
    response = client.post(
        "/api/interview/ask",
        json={"question": "Explain CI/CD", "document": "../secret.pdf"},
    )

    assert response.status_code == 400
    assert "Provide a PDF filename only" in response.json()["detail"]
