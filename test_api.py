from fastapi.testclient import TestClient
from main import app
import pytest
from schemas import Document, SearchRequest
import random

client = TestClient(app)


def test_insert_document():
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


def test_search():
    # Define a sample SearchRequest
    sample_request = SearchRequest(
        query="This is a sample query", collection="test_collection"
    )

    # Send a POST request to the "/text/search" endpoint with the sample SearchRequest
    response = client.post("/text/search", json=sample_request.dict())

    # Check if the response status code is 200
    assert response.status_code == 200
    assert len(response.json())
    assert response.json()[0]["content"] == "This is a sample document"
