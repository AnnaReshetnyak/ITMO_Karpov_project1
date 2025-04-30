import pytest
from sqlmodel import Session, select
from database.models import User, Balance, Transaction
from database.services.crud.user_crud import UserCRUD
from database.services.crud.balance_crud import BalanceCRUD
from exceptions import DuplicateEmailError
from schemas import UserCreate, UserUpdate


@pytest.mark.asyncio
class TestUserCRUD:
    async def test_create_user(self, db_session):
        # Тест создания пользователя
        crud = UserCRUD(db_session)
        user_data = UserCreate(email="test@crud.com", password="password")

        user = await crud.create(user_data)
        assert user.id is not None
        assert user.email == user_data.email
        assert user.is_active is True

    async def test_duplicate_email(self, db_session):
        # Тест дубликата email
        crud = UserCRUD(db_session)
        user_data = UserCreate(email="duplicate@test.com", password="pwd")

        await crud.create(user_data)
        with pytest.raises(DuplicateEmailError):
            await crud.create(user_data)

    async def test_get_user(self, db_session, test_user):
        # Тест получения пользователя
        crud = UserCRUD(db_session)
        user = await crud.get(test_user.id)
        assert user.email == test_user.email

    async def test_update_user(self, db_session, test_user):
        # Тест обновления пользователя
        crud = UserCRUD(db_session)
        update_data = UserUpdate(email="updated@test.com", is_admin=True)

        updated_user = await crud.update(test_user.id, update_data)
        assert updated_user.email == "updated@test.com"
        assert updated_user.is_admin is True

    async def test_delete_user(self, db_session, test_user):
        # Тест удаления пользователя
        crud = UserCRUD(db_session)
        result = await crud.delete(test_user.id)
        assert result is True

        user = await crud.get(test_user.id)
        assert user is None


@pytest.mark.asyncio
class TestBalanceCRUD:
    async def test_balance_operations(self, db_session, test_user):
        # Тест операций с балансом
        crud = BalanceCRUD(db_session)

        # Пополнение
        await crud.make_transaction(test_user.id, 100.0, "deposit", "Initial deposit")
        balance = await crud.get_balance(test_user.id)
        assert balance == 100.0

        # Списание
        await crud.make_transaction(test_user.id, -30.0, "withdraw", "Withdrawal")
        balance = await crud.get_balance(test_user.id)
        assert balance == 70.0

    async def test_insufficient_funds(self, db_session, test_user):
        # Тест недостатка средств
        crud = BalanceCRUD(db_session)
        with pytest.raises(ValueError) as exc_info:
            await crud.make_transaction(test_user.id, -100.0, "withdraw", "Test")

        assert "insufficient funds" in str(exc_info.value).lower()

    async def test_transaction_history(self, db_session, test_user):
        # Тест истории транзакций
        crud = BalanceCRUD(db_session)

        # Создаем несколько транзакций
        transactions = [
            (50.0, "deposit"),
            (-20.0, "withdraw"),
            (100.0, "deposit")
        ]

        for amount, t_type in transactions:
            await crud.make_transaction(test_user.id, amount, t_type, "Test transaction")

        # Проверяем историю
        history = await crud.get_transaction_history(test_user.id)
        assert len(history) == 3
        assert sum(t.amount for t in history) == 130.0


@pytest.mark.asyncio
class TestTransactionRollback:
    async def test_rollback_on_error(self, db_session, test_user):
        # Тест отката транзакции при ошибке
        crud = BalanceCRUD(db_session)
        initial_balance = await crud.get_balance(test_user.id)

        try:
            # Начало транзакции
            await crud.make_transaction(test_user.id, 100.0, "deposit", "Test")
            raise Exception("Simulated error")
        except Exception:
            await db_session.rollback()

            final_balance = await crud.get_balance(test_user.id)
            assert initial_balance == final_balance
