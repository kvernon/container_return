from src.api.models.rental import Rental
from jojanga_queries import rentals


def mapToApiRental(db_rental: rentals.Rental) -> Rental:
    r = Rental()
    r.id = db_rental.id
    r.user_id = db_rental.user_id
    r.asset_id = db_rental.asset_id
    r.created_at_location_id = db_rental.created_at_location_id
    r.created_at = db_rental.created_at
    r.expires_at = db_rental.expires_at
    r.status = db_rental.status
    r.eligible_asset_types = db_rental.eligible_asset_types
    r.returned_at_location_id = db_rental.returned_at_location_id
    r.returned_at = db_rental.returned_at
    return r
