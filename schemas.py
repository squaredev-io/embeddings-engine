from pydantic import BaseModel
from typing import Optional, List, Any
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, JSON
from pgvector.sqlalchemy import Vector


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    embeddings: Optional[List[float]] = Field(
        default=None, sa_column=Column(Vector(384))
    )
    collection: str
    content: str
    source: str
    filters: dict = Field(default=None, sa_column=Column(JSON))


class DeleteDocumentRequest(BaseModel):
    collection: str
    source: str


class SearchRequest(BaseModel):
    query: str
    collection: str
    limit: int
    filters: Optional[dict]


class RecommendationRequest(BaseModel):
    collection: str
    strategy: str = "average_vector"
    limit: int
    filters: Optional[dict]
