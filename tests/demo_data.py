from sqlmodel import Session
from app.database.services.crud import UserCRUD, BalanceCRUD, TransactionCRUD
from app.models.User import User
from app.models.Transaction import Transaction


def create_demo_users(session: Session):
    user_crud = UserCRUD(session)
    balance_crud = BalanceCRUD(session)
    transaction_crud = TransactionCRUD(session)

    # Демо администратор
    if not user_crud.get_by_email("admin@demo.com"):
        admin = user_crud.create(
            email="admin@demo.com",
            hashed_password="admin123",
            is_admin=True
        )
        balance_crud.update(admin.balance.id, 10000.0)

    # Демо пользователь
    if not user_crud.get_by_email("user@demo.com"):
        user = user_crud.create(
            email="user@demo.com",
            hashed_password="user123",
            is_admin=False
        )
        # Создаем демо-транзакции
        transaction_crud.create({
            "user_id": user.id,
            "amount": 1000.0,
            "transaction_type": "deposit"
        })
        transaction_crud.create({
            "user_id": user.id,
            "amount": 500.0,
            "transaction_type": "withdrawal"
        })
        balance_crud.update(user.balance.id, 500.0)

def create_ml_demo_data(session: Session):
    pass
