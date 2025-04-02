from sqlmodel import SQLModel, create_engine, Session, select
from typing import Optional, List
from datetime import datetime
import json
from app.database.models import User, Balance, Transaction, TransactionHistory, MLModel, MLTask, PredictionHistory
from .config import get_db_settings

settings = get_db_settings()
engine = create_engine(settings.DATABASE_URL)

DATABASE_URL = "postgresql://user:password@database:5432/dbname"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class DatabaseManager:
    @staticmethod
    def create_user(email: str, hashed_password: str) -> User:
        with Session(engine) as session:
            user = User(email=email, hashed_password=hashed_password)
            session.add(user)

            # Создаем начальный баланс
            balance = Balance(user=user)
            session.add(balance)

            session.commit()
            session.refresh(user)
            return user

    @staticmethod
    def update_balance(user_id: int, amount: float, transaction_type: str) -> Balance:
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user or not user.balance:
                raise ValueError("User or balance not found")

            # Обновляем баланс
            if transaction_type == "deposit":
                user.balance.amount += amount
            elif transaction_type == "withdrawal":
                if user.balance.amount < amount:
                    raise ValueError("Insufficient funds")
                user.balance.amount -= amount

            # Создаем транзакцию
            transaction = Transaction(
                amount=amount,
                transaction_type=transaction_type,
                user=user
            )

            # Записываем историю
            history = TransactionHistory(
                transaction=transaction,
                balance=user.balance,
                old_amount=user.balance.amount - (amount if transaction_type == "deposit" else -amount),
                new_amount=user.balance.amount
            )

            session.add_all([transaction, history])
            session.commit()
            return user.balance

    @staticmethod
    def get_transaction_history(user_id: int) -> List[Transaction]:
        with Session(engine) as session:
            user = session.get(User, user_id)
            return user.transactions if user else []

    @staticmethod
    def create_ml_model(name: str, owner_id: int, description: Optional[str] = None) -> MLModel:
        with Session(engine) as session:
            model = MLModel(name=name, description=description, owner_id=owner_id)
            session.add(model)
            session.commit()
            return model

    @staticmethod
    def create_ml_task(model_id: int, owner_id: int, input_data: dict) -> MLTask:
        with Session(engine) as session:
            task = MLTask(
                model_id=model_id,
                owner_id=owner_id,
                input_data=json.dumps(input_data),
                status="pending"
            )
            session.add(task)
            session.commit()
            return task

    @staticmethod
    def log_prediction(user_id: int, model_id: int, input_data: dict, result: dict) -> PredictionHistory:
        with Session(engine) as session:
            prediction = PredictionHistory(
                user_id=user_id,
                model_id=model_id,
                input_data=json.dumps(input_data),
                result=json.dumps(result),
                timestamp=datetime.utcnow()
            )
            session.add(prediction)
            session.commit()
            return prediction

    @staticmethod
    def get_user_predictions(user_id: int) -> List[PredictionHistory]:
        with Session(engine) as session:
            statement = select(PredictionHistory).where(PredictionHistory.user_id == user_id)
            return session.exec(statement).all()

    @staticmethod
    def get_model_predictions(model_id: int) -> List[PredictionHistory]:
        with Session(engine) as session:
            statement = select(PredictionHistory).where(PredictionHistory.model_id == model_id)
            return session.exec(statement).all()

init_db()
