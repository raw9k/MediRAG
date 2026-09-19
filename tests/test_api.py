from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={
            "question": "What are the symptoms of diabetes?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0