from fastapi import FastAPI
from typing import List
from embeddings_engine.schemas import (
    DeleteDocumentResponse,
    Document,
    DeleteDocumentRequest,
    RecommendationStrategy,
    SearchRequest,
    RecommendationRequest,
    SearchResponse,
)
from embeddings_engine.settings import get_settings
from sqlmodel import Field, SQLModel, create_engine, select, text, Session
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
        session.commit()

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


@app.post("/text/delete", response_model=DeleteDocumentResponse, tags=["Text"])
async def delete_document(request: DeleteDocumentRequest):
    with Session(engine) as session:
        statement = (
            select(Document)
            .where(Document.collection == request.collection)
            .where(Document.source == request.source)
        )

        results = session.exec(statement)
        for result in results:
            session.delete(result)
        session.commit()

    return {"ok": True}


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
    embedding_model = Embedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        max_length=512,
    )
    positive_embeddings: List[np.ndarray] = list(
        embedding_model.embed(request.positive)
    )
    negative_embeddings: List[np.ndarray] = list(
        embedding_model.embed(request.negative)
    )

    recommendation_vector: List[float] = []  # populated according to request.strategy

    if request.strategy == RecommendationStrategy.average_vector.value:
        positive_embeddings = np.array(positive_embeddings).mean(axis=0).tolist()
        # fill with zeros if no negative embeddings are provided
        negative_embeddings = (
            np.array(negative_embeddings).mean(axis=0).tolist()
            if len(negative_embeddings)
            else np.zeros(384).tolist()
        )

        recommendation_vector = (
            (np.array(positive_embeddings) + np.array(positive_embeddings))
            - np.array(negative_embeddings)
        ).tolist()

    statement = """
            SELECT 1 - (embeddings <=> :embeddings) AS cosine_similarity, content, collection, id, source
            FROM document
            WHERE collection = :collection
        """

    with Session(engine) as session:
        results = session.execute(
            text(statement),
            {
                "collection": request.collection,
                "embeddings": "["
                + str(",".join(str(e) for e in recommendation_vector))
                + "]",
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
