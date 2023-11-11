import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from settings import get_settings
from sqlmodel import Field, SQLModel, create_engine, text, Session
import logging

logger = logging.getLogger(__name__)

settings = get_settings()


@pytest.fixture(scope="module")
def db():
    database_url = settings.DATABASE_URL
    engine = create_engine(database_url, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the tables
    logger.debug("apo prin")
    yield session  # this is where the testing happens
    print("erxesai edw mwrh arxidia?")

    # Teardown: drop the tables and close the connection
    SQLModel.metadata.drop_all(engine)
    session.close()
