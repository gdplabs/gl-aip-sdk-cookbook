from database import connect_db


class UserRepository:
    def __init__(self):
        self.conn = connect_db()
