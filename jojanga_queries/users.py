import sqlite3
from dataclasses import dataclass

from jojanga_queries import db_connection


@dataclass
class User:
    id: str
    name: str


def get_user(id: str) -> User:
    """Get User from database.

    Args:
        id (str): User `id`

    Raises:
        ValueError: If matching user does not exist

    Returns:
        User: User dataclass instance
    """
    try:
        
        cur = db_connection.cursor()
        cur.execute("""SELECT * FROM users WHERE id = ?""", (id,))
        record = cur.fetchone()
        if record:
            return User(*record)
        else:
            raise ValueError("User not found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(e)
    finally:
        cur.close()
