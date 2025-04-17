from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from lesson_2.app.database.services.crud.user_crud import UserCRUD
from lesson_2.app.database.services.crud.prediction import PredictionCRUD
from lesson_2.app.database.database import get_session
from lesson_2.app.models import User
from sqlmodel.ext.asyncio.session import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    # Реализация проверки токена (JWT)
    # Заглушка для примера
    user_crud = UserCRUD(session)
    user = user_crud.get_user_by_email(token)  # В реальности декодирование JWT
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user

async def get_crud(
    session: AsyncSession = Depends(get_session)
) -> PredictionCRUD:
    """Возвращает экземпляр CRUD-класса для предсказаний"""
    return PredictionCRUD(session)
