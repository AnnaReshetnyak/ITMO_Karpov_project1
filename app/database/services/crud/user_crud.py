from sqlmodel import Session, select
from typing import Optional, List
from lesson_2.app.models.User import User
from lesson_2.app.schemas import UserCreate, UserUpdate

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from passlib.context import CryptContext
from lesson_2.app.exceptions import DuplicateEmailError
from lesson_2.app.models import User  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


class UserCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_data: UserCreate) -> User:
        # Проверка существования пользователя
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise DuplicateEmailError(user_data.email)

        # Создание пользователя
        try:
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                # остальные поля
            )
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
            return db_user

        except IntegrityError as e:
            self.session.rollback()
            if "duplicate key" in str(e).lower():
                raise DuplicateEmailError(user_data.email) from e
            raise

    def get(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_all_users(self) -> List[User]:
        result = self.session.exec(select(User))
        return result.all()

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        db_user = self.get(user_id)
        if not db_user:
            return None
        user_data = user_data.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get(user_id)
        if not db_user:
            return False
        self.session.delete(db_user)
        self.session.commit()
        return True
