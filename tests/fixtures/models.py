import pytest
from lesson_2.app.database.models import User, Balance, MLModel

@pytest.fixture
async def test_user(db_session):
    user = User(
        email="fixtureuser@example.com",
        hashed_password="hashedpassword"
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def test_balance(db_session, test_user):
    balance = Balance(amount=100.0, user_id=test_user.id)
    db_session.add(balance)
    await db_session.commit()
    return balance

@pytest.fixture
async def test_ml_model(db_session):
    model = MLModel(name="Test Model", version="1.0")
    db_session.add(model)
    await db_session.commit()
    return model
