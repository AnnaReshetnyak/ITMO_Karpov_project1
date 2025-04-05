import pytest
from sqlmodel import SQLModel, create_engine, Session
from tests.demo_data import create_demo_users

@pytest.fixture(scope="module")
def test_engine():
    return create_engine("sqlite:///test.db")

@pytest.fixture(scope="function")
def test_session(test_engine):
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def demo_session(test_engine):
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        create_demo_users(session)
        yield session
    SQLModel.metadata.drop_all(test_engine)
