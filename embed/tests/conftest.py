import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from embed.settings import get_settings
from sqlmodel import Field, SQLModel, create_engine, text, Session
from embed.main import app
from fastapi.testclient import TestClient


settings = get_settings()


# This fixture is used to create a new database for each test session and drop it after the tests are done.
@pytest.fixture(name="client", scope="session")
def client_fixture():
    database_url = settings.DATABASE_URL
    engine = create_engine(database_url, echo=True)
    SQLModel.metadata.create_all(engine)

    client = TestClient(app)
    yield client
    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()
