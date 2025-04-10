from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.database import get_session
from app.schemas import UserCreate, Token
from app.database.services.crud.user_crud import UserCRUD

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(
        user_data: UserCreate,
        session: Session = Depends(get_session)
):
    user_crud = UserCRUD(session)
    if user_crud.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = user_crud.create(user_data)
    # Генерация JWT токена
    return {"access_token": user.email, "token_type": "bearer"}  # Заглушка


@router.post("/token", response_model=Token)
async def login(
        email: str,
        password: str,
        session: Session = Depends(get_session)
):
    user_crud = UserCRUD(session)
    user = user_crud.authenticate(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return {"access_token": user.email, "token_type": "bearer"}
