from database import connect_db
from models import User


def authenticate_user(username, password):
    conn = connect_db()
    return conn.query(User).filter_by(username=username).first()
