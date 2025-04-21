from lesson_2.app.database.models import User, Balance


def test_user_relationships():
    user = User(email="test@example.com", hashed_password="hash")
    balance = Balance(amount=100.0)

    user.balance = balance

    assert user.balance == balance
    assert balance.user == user


def test_balance_defaults():
    balance = Balance()
    assert balance.amount == 0.0
    assert balance.currency == "credits"
