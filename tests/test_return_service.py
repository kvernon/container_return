from unittest.mock import Mock

import pytest

from repositories.assets_repository import AssetsRepository
from repositories.rentals_repository import RentalsRepository
from repositories.users_repository import UsersRepository
from src.api.models.event import Event
from src.api.models.rental import Rental
from src.services.return_service import ReturnService
from jojanga_queries.assets import Asset
from jojanga_queries.users import User


@pytest.fixture
def user():
    entity = User(
        id="id",
        name="username",
    )
    yield entity


@pytest.fixture
def asset():
    entity = Asset(
        id="id",
        asset_type="clamshell",
    )
    yield entity


@pytest.fixture
def user_repo():
    repository = UsersRepository(None)
    repository.get_user_by_id = Mock(name="get_user_by_id")
    yield repository


@pytest.fixture
def assets_repo():
    repository = AssetsRepository(None)
    repository.get_asset_by_id = Mock(name="get_asset_by_id")
    yield repository


@pytest.fixture
def rental_repo():
    repository = RentalsRepository(None)
    repository.get_rentals_by_user_id = Mock(name="get_rentals_by_user_id")
    repository.get_rental_by_user_id_and_asset_id = Mock(name="get_rental_by_user_id_and_asset_id")
    repository.get_by_id = Mock(name="get_by_id")
    repository.get_in_progress_rentals_for_user = Mock(name="get_in_progress_rentals_for_user")
    repository.update = Mock(name="update")
    yield repository


@pytest.fixture
def return_service(user_repo, assets_repo, rental_repo):
    return_service = ReturnService(user_repo, assets_repo, rental_repo)
    yield return_service


@pytest.fixture
def event():
    evt = Event(
        location_id="location",
        user_qr_data="sdf",
        asset_qr_data="sdf"
    )
    evt.is_valid = Mock(name="is_valid")
    evt.decoded_user_qr_data = Mock(name="decoded_user_qr_data")
    evt.decoded_asset_qr_data = Mock(name="decoded_asset_qr_data")
    yield evt


def test_invalid_event_should_not_run(user, user_repo, asset, assets_repo, return_service):
    user_repo.get_user_by_id.return_value = user
    assets_repo.get_asset_by_id.return_value = asset

    evt = Event()
    return_service.update_rental(evt)

    assert user_repo.get_user_by_id.mock_calls == []
    assert assets_repo.get_asset_by_id.mock_calls == []


def test_invalid_event_should_look_up(user, user_repo, asset, assets_repo, rental_repo, return_service, event):
    user_repo.get_user_by_id.return_value = user
    assets_repo.get_asset_by_id.return_value = asset

    rental = Rental()
    rental.id = "rental+id"
    rental.user_id = "tpg_u0001"
    rental.asset_id = "tpg_a00001"
    rental.eligible_asset_types = ['clamshell']
    rental.is_eligible_for_completion = Mock(name="is_eligible_for_completion")
    rental.is_eligible_for_completion.return_value = True

    rental_repo.get_rental_by_user_id_and_asset_id.return_value = rental
    rental_repo.get_in_progress_rentals_for_user.return_value = [rental]
    rental_repo.update.return_value = None

    event.is_valid.return_value = True
    event.decoded_user_qr_data.return_value = "tpg_u0001"
    event.decoded_asset_qr_data.return_value = "tpg_a00001"

    return_service.update_rental(event)

    assert rental_repo.get_rental_by_user_id_and_asset_id.call_args.args == ('tpg_u0001', 'tpg_a00001',)
    assert assets_repo.get_asset_by_id.call_args.args == ('tpg_a00001',)
    assert rental_repo.update.call_args.args == (rental.id, event.timestamp, event.location_id)
