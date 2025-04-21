import factory
from factory import Faker
from sqlmodel import Session
from lesson_2.app.models import User
from lesson_2.app.models.Transaction import Balance
from lesson_2.app.database.services.crud.user_crud import get_password_hash


class UserFactory(factory.Factory):
    """Фабрика для создания тестовых пользователей"""

    class Meta:
        model = User

    email = Faker("email")
    hashed_password = factory.LazyFunction(lambda: get_password_hash("testpass123"))
    is_active = True
    is_admin = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Кастомный метод для сохранения в базу"""
        session = kwargs.pop("session", None)
        if not session:
            raise ValueError("Необходимо передать сессию базы данных")

        user = model_class(**kwargs)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


class BalanceFactory(factory.Factory):
    """Фабрика для создания тестовых балансов"""

    class Meta:
        model = Balance

    amount = 0.0
    user = factory.SubFactory(UserFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop("session", None)
        if not session:
            raise ValueError("Необходимо передать сессию базы данных")

        balance = model_class(**kwargs)
        session.add(balance)
        session.commit()
        session.refresh(balance)
        return balance
