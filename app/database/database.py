from sqlmodel import SQLModel, create_engine
from app.database.config import get_db_settings

settings = get_db_settings()
engine = create_engine(settings.DATABASE_URL)

DATABASE_URL = "postgresql://user:password@database:5432/dbname"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    session = next(get_session())
    return session
