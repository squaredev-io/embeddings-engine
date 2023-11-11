from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, JSON
from pgvector.sqlalchemy import Vector
import uuid


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    embeddings: Optional[List[float]] = Field(
        default=None, sa_column=Column(Vector(384))
    )
    collection: str
    content: str
    source: str
    filters: dict = Field(default=None, sa_column=Column(JSON))


class SearchResponse(BaseModel):
    id: int
    cosine_similarity: float
    content: str
    collection: str
    source: str


class DeleteDocumentRequest(BaseModel):
    collection: str
    source: str


class SearchRequest(BaseModel):
    query: str
    collection: str
    limit: Optional[int] = 5
    filters: Optional[dict] = None


class RecommendationRequest(BaseModel):
    collection: str
    strategy: str = "average_vector"
    limit: int
    filters: Optional[dict]
