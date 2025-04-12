from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

# --------------------------
# Базовый конфиг для всех схем
# --------------------------
class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # заменяет orm_mode
        protected_namespaces=()  # отключает проверку protected namespaces
    )

# --------------------------
# User Schemas
# --------------------------
class UserBase(BaseSchema):
    email: EmailStr = Field(..., example="user@example.com")
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="securepassword123")

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8, example="newpassword123")
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserOut(UserBase):
    id: int
    created_at: datetime

# --------------------------
# Balance Schemas
# --------------------------
class BalanceBase(BaseSchema):
    amount: float = Field(..., ge=0, example=1000.0)
    currency: str = Field(default="USD", max_length=3)

class BalanceCreate(BalanceBase):
    user_id: int = Field(..., example=1)

class BalanceUpdate(BalanceBase):
    amount: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)

class BalanceOut(BalanceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class TopUpRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to top up")

class BalanceResponse(BaseModel):
    balance: float

# --------------------------
# Transaction Schemas
# --------------------------
class TransactionBase(BaseSchema):
    amount: float = Field(..., gt=0, example=100.0)
    transaction_type: str = Field(..., example="deposit")
    description: Optional[str] = Field(None, example="Payment for services")

class TransactionCreate(TransactionBase):
    user_id: int = Field(..., example=1)

class TransactionUpdate(BaseSchema):
    description: Optional[str] = None
    status: Optional[str] = None  # pending, completed, failed

class TransactionOut(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    status: str

# --------------------------
# Transaction History Schemas
# --------------------------
class TransactionHistoryBase(BaseSchema):
    old_amount: float
    new_amount: float

class TransactionHistoryCreate(TransactionHistoryBase):
    transaction_id: int = Field(..., example=1)
    balance_id: int = Field(..., example=1)

class TransactionHistoryOut(TransactionHistoryBase):
    id: int
    transaction_id: int
    balance_id: int
    created_at: datetime

# --------------------------
# ML Model Schemas (решение конфликта model_)
# --------------------------
class MLModelBase(BaseSchema):
    name: str = Field(..., example="Credit Scoring Model")
    description: Optional[str] = Field(None, example="Predicts creditworthiness")
    version: str = Field(default="1.0", example="2.1")

class MLModelCreate(MLModelBase):
    owner_id: int = Field(..., example=1)

class MLModelUpdate(BaseSchema):
    description: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = True

class MLModelOut(MLModelBase):
    id: int
    owner_id: int
    created_at: datetime
    is_active: bool

# --------------------------
# ML Task Schemas
# --------------------------
class MLTaskBase(BaseSchema):
    input_data: Dict[str, Any] = Field(..., example={"income": 50000, "age": 30})
    priority: int = Field(default=1, ge=1, le=5)

class MLTaskCreate(MLTaskBase):
    ml_model_id: int = Field(..., example=1, alias="model_id")  # Решение конфликта имен
    user_id: int = Field(..., example=1)

class MLTaskUpdate(BaseSchema):
    status: Optional[str] = Field(None, example="completed")
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class MLTaskOut(MLTaskBase):
    id: int
    ml_model_id: int = Field(alias="model_id")
    user_id: int
    created_at: datetime
    status: str
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
# --------------------------
# Prediction History Schemas
# --------------------------
class PredictionHistoryBase(BaseSchema):
    input_data: Dict[str, Any] = Field(..., example={"transaction_id": 123})
    result: Dict[str, Any] = Field(..., example={"risk_score": 0.85})

class PredictionHistoryCreate(PredictionHistoryBase):
    user_id: int = Field(..., example=1)
    ml_model_id: int = Field(..., example=1, alias="model_id")  # Решение конфликта имен
    task_id: Optional[int] = None

class PredictionHistoryUpdate(BaseSchema):
    feedback: Optional[Dict[str, Any]] = None  # User feedback on prediction

class PredictionHistoryOut(PredictionHistoryBase):
    id: int
    user_id: int
    ml_model_id: int = Field(alias="model_id")
    task_id: Optional[int]
    created_at: datetime
    feedback: Optional[Dict[str, Any]]

# --------------------------
# Auth Schemas
# --------------------------
class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenData(BaseSchema):
    user_id: Optional[int] = None
