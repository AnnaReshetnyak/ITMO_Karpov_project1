from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.config import get_settings
from lesson_2.app.models.Transaction import Transaction
from lesson_2.app.models.MLSegment import PredictionHistory
from typing import Dict, Any
from sqlalchemy.orm import sessionmaker, declarative_base

# Настройка асинхронного движка
engine = create_engine(
    get_settings.DATABASE_URL,
    echo=True,
    future=True
)

# Асинхронная сессия
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_prediction(
        prediction_data: Dict[str, Any],
        session: AsyncSession
) -> PredictionHistory:
    """Сохранение результата предсказания в БД"""
    try:
        # Создаем запись о предсказании
        prediction = PredictionHistory(
            user_id=prediction_data["user_id"],
            input_data=prediction_data["input"],
            result=prediction_data["result"],
            cost=prediction_data.get("cost", 0.0),
            model_version=prediction_data.get("model_version", "1.0")
        )

        # Создаем транзакцию
        transaction = Transaction(
            user_id=prediction_data["user_id"],
            amount=-prediction_data.get("cost", 0.0),
            type="PREDICTION",
            description=f"Prediction #{prediction.id}"
        )

        session.add(prediction)
        session.add(transaction)
        await session.commit()
        await session.refresh(prediction)

        return prediction
    except Exception as e:
        await session.rollback()
        raise e
