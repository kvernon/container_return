from python_event_bus import EventBus

from repositories.assets_repository import AssetsRepository
from repositories.rentals_repository import RentalsRepository
from repositories.users_repository import UsersRepository
from src.api.models.event import Event
from src.api.models.rental_filters import get_first_match
from src.services.event_names import EventNames

# acceptable_types = [
#     '3-compartment',
#     'clamshell',
#     'large-bowl',
#     'mug',
#     'small-bowl'
# ]

class ReturnService:

    def __init__(self, user_repo: UsersRepository, assets_repo: AssetsRepository, rental_repo: RentalsRepository):
        self.user_repo = user_repo
        self.assets_repo = assets_repo
        self.rental_repo = rental_repo

    def update_rental(self, event: Event):
        print("===================")
        print("EVENT FIRED for update_rental")
        print("===================")

        if event is None:
            print("event is none")
            return

        if not event.is_valid():
            print("event is invalid")
            return

        asset_id = event.decoded_asset_qr_data()
        user_id = event.decoded_user_qr_data()

        returned_rental = self.rental_repo.get_rental_by_user_id_and_asset_id(user_id, asset_id)

        if returned_rental is None or not returned_rental.is_eligible_for_completion(event.get_date()):
            print("returned_rental is none or not eligible for completion")
            return

        in_progress_rentals = self.rental_repo.get_in_progress_rentals_for_user(user_id)

        asset = self.assets_repo.get_asset_by_id(asset_id)

        # grab first item that matches
        first_match = get_first_match(in_progress_rentals, asset.asset_type)

        if first_match is None:
            return

        self.rental_repo.update(first_match.id, event.timestamp, event.location_id)
        EventBus.call(EventNames.RENTAL_RETURN_COMPLETE, event)
