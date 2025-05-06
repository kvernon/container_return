from data_layers.db_users import DbUsers
from jojanga_queries.users import User


class UsersRepository:
    def __init__(self, users_query: DbUsers):
        self.users_query = users_query

    def get_user_by_id(self, user_id: str) -> User | None:
        try:
            user = self.users_query.get_user(user_id)

            if User is None:
                return None

            return user
        except Exception:
            print("get_user_by_id failed")
            return None
