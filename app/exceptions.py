from fastapi import HTTPException
from starlette import status

class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


class InsufficientFundsError(Exception):
    def __init__(self, balance: float):
        self.balance = balance
        super().__init__(f"Insufficient funds. Current balance: {balance}")


class DuplicateEmailError(Exception):
    """Ошибка дублирования email в базе данных"""
    def __init__(self, email: str):
        self.email = email
        message = f"Email {email} already registered"
        super().__init__(message)
