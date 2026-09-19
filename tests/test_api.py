from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={"question": "What are the symptoms of diabetes?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0


def test_ask_endpoint_rejects_short_question():
    response = client.post(
        "/ask",
        json={"question": "Hi"},
    )

    assert response.status_code == 422
    
def test_ask_endpoint_rejects_out_of_context_question():
    response = client.post(
        "/ask",
        json={"question": "What is the capital of France?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        "does not provide enough information"
        in data["answer"].lower()
    )

    assert data["sources"] == []