from dataclasses import dataclass
import sqlite3
from typing import List

from jojanga_queries import db_connection


@dataclass
class Rental:
    id: str
    user_id: str
    asset_id: str
    created_at_location_id: str
    created_at: str
    expires_at: str
    status: str
    eligible_asset_types: list
    returned_at_location_id: str
    returned_at: str

    def __post_init__(self):
        # SQLite only stores primitive types;
        # convert JSON array string to Python list
        self.eligible_asset_types = list(eval(self.eligible_asset_types))


def get_rental(id: str) -> Rental:
    print(f"getting rental for id: {id}")
    """Get Rental from database.

    Args:
        id (str): Rental `id`

    Raises:
        ValueError: Matching rental does not exist

    Returns:
        Rental: Rental dataclss instance
    """
    try:
        cur = db_connection.cursor()
        print(f"cursor acquired for rental id: {id}")
        print(f"executing query for rental id: {id}")
        cur.execute("SELECT * FROM rentals WHERE id = ?", (id,))
        print(f"executed query for rental id: {id}")
        record = cur.fetchone()
        print(record)
        if record:
            print(f"rental record found for id: {id}")
            return Rental(*record)
        else:
            print(f"rental record not found: {id}")
            raise ValueError("Rental not found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(e)
    finally:
        cur.close()


def list_rentals_for_user(user_id: str) -> List[Rental]:
    """List all Rentals for a user.

    Feel free to extend or modify this helper as you see fit.
    Changing this is not necessary for completing this challenge.
    But if you do, please include a note about the change(s) in your deliverable.

    Args:
        user_id (str): User `id` to list Rentals for

    Returns:
        List[Rental]: Array of Rental dataclass instances
    """
    try:
        cur = db_connection.cursor()
        cur.execute("SELECT * FROM rentals where user_id = ?", (user_id,))
        records = cur.fetchall()
        return [Rental(*record) for record in records]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(e)
    finally:
        cur.close()


def get_in_progress_rentals_for_user(user_id: str) -> List[Rental]:
    try:
        print(f"cursor acquired for user_id: {user_id}")
        cur = db_connection.cursor()
        print(f"executing query for user_id: {user_id}")
        cur.execute("SELECT * FROM rentals where user_id = ? AND status like 'IN_PROGRESS' ORDER BY date(expires_at)",
                    (user_id,))
        print(f"executed query for user_id: {user_id}")
        records = cur.fetchall()
        for entry in records:
            for column in entry:
                print(f"(raw) entry[{column}]")

        return [Rental(*record) for record in records]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(e)
    finally:
        cur.close()


def get_rental_for_user_with_asset_id(user_id: str, asset_id: str) -> Rental:
    try:
        cur = db_connection.cursor()
        cur.execute("SELECT * FROM rentals WHERE user_id = ? AND asset_id = ?", (user_id, asset_id))
        record = cur.fetchone()
        if record:
            return Rental(*record)
        else:
            raise ValueError("Rental not found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(e)
    finally:
        cur.close()


def complete_rental(
        id: str, status: str, returned_at: str, returned_at_location_id: str
) -> None:
    """Complete Rental with provided args.

    Args:
        id (str): Rental `id` to update
        status (str): {'FORGIVEN', 'FLAGGED', 'COMPLETED'}
        returned_at (str): ISO8601 timestamp of return
        returned_at_location_id (str): Location ID of return
    """
    try:

        cur = db_connection.cursor()
        cur.execute(
            """
                    UPDATE rentals
                    SET status = ?,
                        returned_at = ?,
                        returned_at_location_id = ?
                    WHERE id = ?
                    """,
            (status, returned_at, returned_at_location_id, id),
        )
        db_connection.commit()
        cur.close()
        return get_rental(id)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(e)
    finally:
        cur.close()
