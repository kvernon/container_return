from typing import List

from data_layers.db_rentals import DbRental
from src.api.models.rental import Rental
from src.encoders.translate_rentals import mapToApiRental

class RentalsRepository:
    def __init__(self, rentals_query: DbRental):
        self.rentals_query = rentals_query

    def get_rentals_by_user_id(self, user_id: str) -> List[Rental]:
        the_rentals = self.rentals_query.list_rentals_for_user(user_id)
        return list(map(mapToApiRental, the_rentals))

    def get_rental_by_user_id_and_asset_id(self, user_id: str, asset_id: str) -> Rental | None:
        rental = self.rentals_query.get_rental_for_user_with_asset_id(user_id, asset_id)
        if rental is None:
            return None
        return mapToApiRental(rental)

    def get_in_progress_rentals_for_user(self, user_id: str) -> List[Rental]:
        print(f"get_in_progress_rentals_for_user user_id: {user_id}")
        the_rentals = self.rentals_query.get_in_progress_rentals_for_user(user_id)
        for mapped_rental in the_rentals:
            print(f"(get_in_progress_rentals_for_user) the_rentals: {mapped_rental.id} returned_at:{mapped_rental.returned_at} returned_at_location_id:{mapped_rental.returned_at_location_id}")

        print(f"the_rentals length: {len(the_rentals)}")
        mapped = list(map(mapToApiRental, the_rentals))
        for mapped_rental in mapped:
            print(f"(get_in_progress_rentals_for_user) mapped_rental: {mapped_rental.id} returned_at:{mapped_rental.returned_at} returned_at_location_id:{mapped_rental.returned_at_location_id}")

        return mapped

    def get_by_id(self, rental_id: str) -> Rental | None:
        rental = self.rentals_query.get_rental(rental_id)
        if rental is None:
            return None
        return mapToApiRental(rental)

    def update(self, rental_id: str, returned_at: str, returned_at_location_id: str):
        self.rentals_query.complete_rental(
            rental_id,
            'COMPLETED',
            returned_at,
            returned_at_location_id
        )
