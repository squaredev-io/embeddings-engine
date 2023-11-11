from fastapi import FastAPI
from typing import List
from schemas import (
    Document,
    DeleteDocumentRequest,
    SearchRequest,
    RecommendationRequest,
)
from settings import get_settings
from sqlmodel import Field, SQLModel, create_engine, select, Session
from fastembed.embedding import FlagEmbedding as Embedding
from typing import List
import numpy as np

settings = get_settings()

database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()
settings = get_settings()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


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
        session.refresh(documents)
    return documents


@app.post("/text/delete", response_model=List[Document], tags=["Text"])
async def delete_document(request: DeleteDocumentRequest):
    # Implement your logic here
    return []


@app.post("/text/search", response_model=List[Document], tags=["Text"])
async def search(request: SearchRequest):
    # Implement your logic here
    return []


@app.post("/text/recommend", response_model=List[Document], tags=["Text"])
async def recommend(request: RecommendationRequest):
    # Implement your logic here
    return []
