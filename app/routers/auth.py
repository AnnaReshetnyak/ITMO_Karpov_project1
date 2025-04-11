from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.database import get_session
from app.schemas import UserCreate, Token
from app.database.services.crud.user_crud import UserCRUD
from fastapi.security import OAuth2PasswordRequestForm

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
    return {"access_token": user.email, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    user_crud = UserCRUD(session)
    user = user_crud.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return {"access_token": user.email, "token_type": "bearer"}
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return {"access_token": user.email, "token_type": "bearer"}
