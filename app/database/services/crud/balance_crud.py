from database.models import Transaction
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

class BalanceCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_balance(self, user_id: str) -> float:
        """Получение текущего баланса"""
        statement = select(func.coalesce(func.sum(Transaction.amount), 0.0)).where(
            Transaction.user_id == user_id
        )
        result = await self.session.exec(statement)
        return result.one()

    async def make_transaction(
        self,
        user_id: str,
        amount: float,
        type: str,
        description: str
    ) -> Transaction:
        """Создание транзакции"""
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=type,
            description=description
        )
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction
