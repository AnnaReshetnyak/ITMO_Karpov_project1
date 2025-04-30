from database.config import get_db_settings
from database.database import get_session, init_db, engine
from database.services.crud.user import get_all_users, create_user
from sqlmodel import Session
from models.User import User

if __name__ == "__main__":
    test_user = User(email='test1@mail.ru', password='test')
    test_user_2 = User(email='test2@mail.ru', password='test')
    test_user_3 = User(email='test3@mail.ru', password='test')

    settings = get_db_settings()
    print(settings.DB_HOST)
    print(settings.DB_NAME)

    init_db()
    print('Init db has been success')

    with Session(engine) as session:
        create_user(test_user, session)
        create_user(test_user_2, session)
        create_user(test_user_3, session)
        users = get_all_users(session)

    print('-------------------')
    print(id(test_user) == id(users[0]))
    print(id(test_user))
    print(id(users[0]))

    for user in users:
        print(f'id: {user.id} - {user.email}')
        print(type(user))
        print(user.say[0])
