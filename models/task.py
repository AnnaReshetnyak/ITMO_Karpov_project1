from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from lesson_2.app.schemas import TaskStatus

class MLTaskBase(SQLModel):
    cost: float = Field(default=0.0, ge=0)
    user_id: UUID = Field(foreign_key="users.id")
    input_data: dict = Field(sa_column=Column(JSON))
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        sa_column=Column(SQLEnum(TaskStatus)),
        index=True
    )
    result: Optional[dict] = None

class MLTask(MLTaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
