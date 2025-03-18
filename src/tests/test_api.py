import pytest
from fastapi.testclient import TestClient
from src.api.endpoints import app
# from src.rag.chat import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat", json={"query": "nước hoa cho nam mùi hương nhẹ nhàng?"})
    print('==== response ====')
    print(response.json())
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)

def test_chat_empty_query():
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Query is required"
