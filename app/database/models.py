from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime



class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    balance: Optional["Balance"] = Relationship(back_populates="user", sa_relationship_kwargs={'uselist': False})
    transactions: List["Transaction"] = Relationship(back_populates="user")
    ml_tasks: List["MLTask"] = Relationship(back_populates="owner")
    predictions: List["PredictionHistory"] = Relationship(back_populates="user")



class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(default=0.0, ge=0)
    currency: str = Field(default="USD")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="balance")
    history: List["TransactionHistory"] = Relationship(back_populates="balance")


class TransactionBase(SQLModel):
    amount: float
    transaction_type: str  # deposit, withdrawal, transfer
    description: Optional[str] = None


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="transactions")
    history: List["TransactionHistory"] = Relationship(back_populates="transaction")


class TransactionHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transaction.id")
    balance_id: int = Field(foreign_key="balance.id")
    old_amount: float
    new_amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    transaction: Transaction = Relationship(back_populates="history")
    balance: Balance = Relationship(back_populates="history")


class MLModelBase(SQLModel):
    name: str
    description: Optional[str] = None
    version: str = "1.0"


class MLModel(MLModelBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    tasks: List["MLTask"] = Relationship(back_populates="model")
    predictions: List["PredictionHistory"] = Relationship(back_populates="model")


class MLTaskBase(SQLModel):
    name: str
    status: str = "pending"  # pending, running, completed, failed
    input_data: str  # JSON string or reference to storage


class MLTask(MLTaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    model_id: Optional[int] = Field(default=None, foreign_key="mlmodel.id")

    owner: Optional[User] = Relationship(back_populates="ml_tasks")
    model: Optional[MLModel] = Relationship(back_populates="tasks")


class PredictionHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    model_id: int = Field(foreign_key="mlmodel.id")
    input_data: str  # JSON-строка
    result: str  # JSON-строка
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="predictions")
    model: MLModel = Relationship(back_populates="predictions")
