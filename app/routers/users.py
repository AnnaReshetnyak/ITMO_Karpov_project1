from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database.database import get_session
from app.models import User
from app.schemas import UserUpdate
from app.dependencies import get_current_user
from app.database.services.crud.user_crud import UserCRUD

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.patch("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user_crud = UserCRUD(session)
    return user_crud.update(current_user.id, user_data)


@user_router.get('/get_all_users', response_model=List[User])
async def get_all_users(session=Depends(get_session)) -> list:
    return UserService.get_all_users(session)
