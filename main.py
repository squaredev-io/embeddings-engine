from fastapi import FastAPI
from typing import List
from schemas import (
    Document,
    DeleteDocumentRequest,
    SearchRequest,
    RecommendationRequest,
    SearchResponse,
)
from settings import get_settings
from sqlmodel import Field, SQLModel, create_engine, text, Session
from fastembed.embedding import FlagEmbedding as Embedding
from typing import List
import numpy as np

settings = get_settings()

database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo=True)


app = FastAPI()
settings = get_settings()


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        statement = "CREATE EXTENSION IF NOT EXISTS vector;"
        results = session.execute(text(statement))
    SQLModel.metadata.create_all(engine)


@app.post("/text", response_model=List[Document], tags=["Text"])
async def insert_document(documents: List[Document]):
    embedding_model = Embedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        max_length=512,
    )
    embeddings: List[np.ndarray] = list(
        embedding_model.embed([d.content for d in documents])
    )

    # Map documents.content to embeddings
    for document, embedding in zip(documents, embeddings):
        document.embeddings = embedding.tolist()

    with Session(engine) as session:
        session.bulk_save_objects(documents)
        session.commit()
    return documents


@app.post("/text/delete", response_model=List[Document], tags=["Text"])
async def delete_document(request: DeleteDocumentRequest):
    # Implement your logic here
    return []


@app.post("/text/search", response_model=List[SearchResponse], tags=["Text"])
async def search(request: SearchRequest):
    with Session(engine) as session:
        embedding_model = Embedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            max_length=512,
        )

        embeddings: List[np.ndarray] = list(embedding_model.embed([request.query]))
        embeddings = embeddings[0].tolist()

        statement = """
            SELECT 1 - (embeddings <=> :embeddings) AS cosine_similarity, content, collection, id, source
            FROM document
            WHERE collection = :collection
        """

        results = session.execute(
            text(statement),
            {
                "collection": request.collection,
                "embeddings": "[" + str(",".join(str(e) for e in embeddings)) + "]",
            },
        )
        session.commit()

    search_response = [
        SearchResponse(
            **{
                "cosine_similarity": r[0],
                "content": r[1],
                "collection": r[2],
                "id": r[3],
                "source": r[4],
            }
        )
        for r in results
    ]

    return search_response


@app.post("/text/recommend", response_model=List[Document], tags=["Text"])
async def recommend(request: RecommendationRequest):
    # Implement your logic here
    return []
