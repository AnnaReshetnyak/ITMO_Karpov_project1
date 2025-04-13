from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class PredictionBase(SQLModel):
    user_id: UUID = Field(foreign_key="users.id")
    input_data: dict
    result: dict
    cost: float = Field(default=0.0, ge=0)
    model_version: str = Field(default="1.0", max_length=50)

class Prediction(PredictionBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
