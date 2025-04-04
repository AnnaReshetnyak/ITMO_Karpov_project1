from sqlmodel import Session, select
from typing import Optional, List
from app.models import User
from app.schemas import UserCreate, UserUpdate



class UserCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_data: UserCreate) -> User:
        db_user = User(**user_data.dict())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_all(self) -> List[User]:
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
