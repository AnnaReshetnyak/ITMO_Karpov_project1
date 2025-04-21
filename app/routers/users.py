from fastapi import APIRouter, Depends, status, Security, Request, HTTPException
from sqlmodel import Session
from lesson_2.app.database.database import get_session
from lesson_2.app.exceptions import DuplicateEmailError
from lesson_2.app.models import User
from lesson_2.app.schemas import UserUpdate, UserCreate
from lesson_2.app.dependencies import get_current_user
from lesson_2.app.database.services.crud.user_crud import UserCRUD
import logging
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def read_current_user(
        request: Request,
        current_user: User = Depends(get_current_user)
):
    """Получение информации о текущем пользователе"""
    try:
        logger.info(
            f"User profile request - UserID: {current_user.id} | "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        return current_user

    except Exception as e:
        logger.error(
            f"Failed to get user profile - UserID: {current_user.id} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=List[User])
async def get_all_users(
        request: Request,
        session: Session = Depends(get_session),
        current_user: User = Security(get_current_user, scopes=["admin"])
):
    """Получение списка всех пользователей (только для админов)"""
    try:
        logger.info(
            f"All users request - AdminID: {current_user.id} | "
            f"Client: {request.client.host}"
        )

        if not current_user.is_admin:
            logger.warning(
                f"Unauthorized admin access attempt - UserID: {current_user.id} | "
                f"Email: {current_user.email}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        user_crud = UserCRUD(session)
        users = user_crud.get_all_users()

        logger.debug(
            f"Retrieved {len(users)} users - AdminID: {current_user.id}"
        )
        return users

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to get users list - AdminID: {current_user.id} | "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.patch("/me", response_model=User)
async def update_current_user(
        request: Request,
        user_data: UserUpdate,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Обновление данных текущего пользователя"""
    try:
        logger.info(
            f"User update request - UserID: {current_user.id} | "
            f"Fields: {user_data.dict(exclude_unset=True)} | "
            f"Client: {request.client.host}"
        )

        user_crud = UserCRUD(session)
        updated_user = user_crud.update(current_user.id, user_data)

        logger.info(
            f"User updated successfully - UserID: {current_user.id} | "
            f"Updated fields: {user_data.dict(exclude_unset=True)}"
        )
        return updated_user

    except Exception as e:
        logger.error(
            f"Failed to update user - UserID: {current_user.id} | "
            f"Error: {str(e)} | "
            f"Input data: {user_data.dict()}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user data"
        )


async def create_user(user_data: UserCreate):
    """Создание нового пользователя (внутренний метод)"""
    logger.info("Creating new user: %s", user_data.email)
    try:
        #создание пользователя ...
        logger.debug("User created successfully")
    except DuplicateEmailError:
        logger.warning("Duplicate email: %s", user_data.email)
        raise
    except Exception as e:
        logger.error(
            "User creation failed: %s | Data: %s",
            str(e),
            user_data.dict(exclude={'password'}),
            exc_info=True
        )
        raise
