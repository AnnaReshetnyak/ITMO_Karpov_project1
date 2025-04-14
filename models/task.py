from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class MLTaskBase(SQLModel):
    user_id: UUID = Field(foreign_key="users.id")
    input_data: dict = Field(sa_column=Column(JSON))
    status: str = Field(default="pending", index=True)
    result: Optional[dict] = None
    model_version: str = Field(default="1.0", max_length=20)


class MLTask(MLTaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
