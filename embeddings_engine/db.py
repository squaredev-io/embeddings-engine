from embeddings_engine.settings import get_settings
from sqlmodel import create_engine

settings = get_settings()

database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo=True)
