from typing import List

from jojanga_queries import rentals


class DbRental:
    def __init__(self):
        pass

    def get_rental(self, rental_id: str) -> rentals.Rental | None:
        try:
            return rentals.get_rental(rental_id)
        except Exception:
            print("get_rental failed")
            return None

    def list_rentals_for_user(self, user_id: str) -> List[rentals.Rental]:
        return rentals.list_rentals_for_user(user_id)

    def get_in_progress_rentals_for_user(self, user_id: str) -> List[rentals.Rental]:
        return rentals.get_in_progress_rentals_for_user(user_id)

    def get_rental_for_user_with_asset_id(self, user_id: str, asset_id: str) -> rentals.Rental | None:
        try:
            return rentals.get_rental_for_user_with_asset_id(user_id, asset_id)
        except Exception:
            return None

    def complete_rental(self, rental_id: str, status: str, returned_at: str, returned_at_location_id: str) -> None:
        return rentals.complete_rental(rental_id, status, returned_at, returned_at_location_id)
