from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False

    model_config = ConfigDict(
        protected_namespaces=()
    )


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: Optional["Balance"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")
    ml_tasks: List["MLTask"] = Relationship(back_populates="owner")


class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(default=0.0, ge=0)
    currency: str = Field(default="credits")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="balance")
    history: List["TransactionHistory"] = Relationship(back_populates="balance")

    model_config = ConfigDict(
        protected_namespaces=()
    )

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    transaction_type: str
    description: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="transactions")
    history: List["TransactionHistory"] = Relationship(back_populates="transaction")

    model_config = ConfigDict(
        protected_namespaces=()
    )

class TransactionHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transaction.id")
    balance_id: int = Field(foreign_key="balance.id")
    old_amount: float
    new_amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    transaction: Transaction = Relationship(back_populates="history")
    balance: Balance = Relationship(back_populates="history")

    model_config = ConfigDict(
        protected_namespaces=()
    )

class MLModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    tasks: List["MLTask"] = Relationship(back_populates="model")
    predictions: List["PredictionHistory"] = Relationship(back_populates="model")

    model_config = ConfigDict(
        protected_namespaces=()
    )


class MLTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str = "pending"
    input_data: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    ml_model_id: Optional[int] = Field(default=None, foreign_key="mlmodel.id")

    owner: Optional[User] = Relationship(back_populates="ml_tasks")
    model: Optional["MLModel"] = Relationship(back_populates="tasks")

    model_config = ConfigDict(
        protected_namespaces=()
    )
