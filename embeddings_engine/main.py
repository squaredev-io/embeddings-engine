from fastapi import FastAPI
from embeddings_engine.settings import get_settings
from sqlmodel import Field, SQLModel, create_engine, select, text, Session
from embeddings_engine.v1 import v1_router
from embeddings_engine.db import engine

settings = get_settings()


app = FastAPI()
settings = get_settings()

app.include_router(v1_router)


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        statement = "CREATE EXTENSION IF NOT EXISTS vector;"
        results = session.execute(text(statement))
        session.commit()

    SQLModel.metadata.create_all(engine)
