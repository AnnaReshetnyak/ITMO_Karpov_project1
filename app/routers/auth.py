import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from lesson_2.app.database.database import get_session
from lesson_2.app.schemas import UserCreate, Token
from lesson_2.app.database.services.crud.user_crud import UserCRUD
from fastapi.security import OAuth2PasswordRequestForm

# Инициализация логгера
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(
        request: Request,
        user_data: UserCreate,
        session: Session = Depends(get_session)
):
    """Регистрация нового пользователя с логированием"""
    try:
        logger.info(
            f"Registration attempt - Email: {user_data.email} | "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        user_crud = UserCRUD(session)

        # Проверка существующего пользователя
        if existing_user := user_crud.get_user_by_email(user_data.email):
            logger.warning(
                f"Duplicate registration attempt - Email: {user_data.email} | "
                f"Existing user ID: {existing_user.id}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Создание пользователя
        user = user_crud.create(user_data)
        logger.info(
            f"User registered successfully - ID: {user.id} | "
            f"Email: {user.email}"
        )

        return {"access_token": user.email, "token_type": "bearer"}

    except Exception as e:
        logger.error(
            f"Registration error - Email: {user_data.email} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise


@router.post("/login", response_model=Token)
async def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """Аутентификация пользователя с логированием"""
    try:
        logger.info(
            f"Login attempt - Email: {form_data.username} | "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        user_crud = UserCRUD(session)
        user = user_crud.authenticate(form_data.username, form_data.password)

        if not user:
            logger.warning(
                f"Failed login attempt - Email: {form_data.username} | "
                f"Reason: Invalid credentials"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        logger.info(
            f"Successful login - User ID: {user.id} | "
            f"Email: {user.email}"
        )

        return {"access_token": user.email, "token_type": "bearer"}

    except HTTPException:
        # Повторно вызываем исключение, так как оно уже залогировано
        raise

    except Exception as e:
        logger.error(
            f"Login error - Email: {form_data.username} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
