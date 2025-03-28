import bcrypt
from typing import List, Dict

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._password_hash = self._hash_password(password)
        self.transaction_history = TransactionHistory(user_id)
        self.balance = Balance(self.transaction_history)

    @property
    def user_id(self) -> int:
        return self._user_id

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self._password_hash)

class Admin(User):
    def view_user_history(self, user: User) -> List[Dict]:
        return user.transaction_history.get_history()
