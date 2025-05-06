from typing import List

from src.api.models.rental import Rental


def get_first_match(in_progress_rentals: List[Rental], asset_type: str) -> Rental | None:
    for rental in in_progress_rentals:
        if asset_type in rental.eligible_asset_types:
            return rental

    return None
