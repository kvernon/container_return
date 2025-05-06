from jojanga_queries import users


class DbUsers:
    def __init__(self):
        pass

    def get_user(self, user_id: str) -> users.User:
        return users.get_user(user_id)
