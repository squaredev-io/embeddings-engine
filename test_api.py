from fastapi.testclient import TestClient
from schemas import Document, RecommendationRequest, SearchRequest


def test_insert_document(client: TestClient):
    sample_document_1 = Document(
        id=0,
        content="This is a sample document",
        filters={"author": "John Doe"},
        source="example.txt",
        collection="test_collection",
    )

    sample_document_2 = Document(
        id=1,
        content="some other content",
        filters={"author": "John Doe"},
        source="example2.txt",
        collection="test_collection",
    )

    response = client.post(
        "/text",
        json=[
            sample_document_1.dict(),
            sample_document_2.dict(),
        ],
    )

    assert response.status_code == 200
    assert response.json()[0]["content"] == sample_document_1.content
    assert response.json()[0]["collection"] == sample_document_1.collection


def test_search(client: TestClient):
    # Define a sample SearchRequest
    sample_request = SearchRequest(
        query="This is a sample query", collection="test_collection"
    )

    response = client.post("/text/search", json=sample_request.dict())

    assert response.status_code == 200
    assert len(response.json())
    assert response.json()[0]["content"] == "This is a sample document"


def test_recommend(client: TestClient):
    sample_request = RecommendationRequest(
        positive=["This is a sample query"],
        collection="test_collection",
    )

    response = client.post("/text/recommend", json=sample_request.dict())

    assert response.status_code == 200
    assert len(response.json())
    assert response.json()[0]["content"] == "This is a sample document"
