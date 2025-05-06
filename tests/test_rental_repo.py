from unittest.mock import Mock, patch

import pytest
from jojanga_queries import rentals

from repositories.rentals_repository import RentalsRepository
from jojanga_queries.rentals import Rental
from src.api.models import rental


@pytest.fixture()
def query():
    the_rentals = rentals
    the_rentals.list_rentals_for_user = Mock(name="list_rentals_for_user")
    the_rentals.get_rental = Mock(name="get_rental")
    the_rentals.get_in_progress_rentals_for_user = Mock(name="get_in_progress_rentals_for_user")
    the_rentals.complete_rental = Mock(name="complete_rental")
    yield the_rentals


@pytest.fixture()
def db_rental():
    with patch.object(Rental, '__post_init__'):
        dbRental = Rental(
            id="R1",
            user_id="something",
            asset_id="asset_id",
            created_at_location_id="created_at_location_id",
            created_at="created_at",
            expires_at="expires_at",
            eligible_asset_types=[],
            status="status",
            returned_at_location_id="returned_at_location_id",
            returned_at="returned_at",
        )

    return dbRental


def test_should_call_get_in_progress_rentals_for_user(query, db_rental):
    query.get_in_progress_rentals_for_user.return_value = [db_rental]
    repo = RentalsRepository(query)
    actual_rentals = repo.get_in_progress_rentals_for_user(db_rental.user_id)
    assert isinstance(actual_rentals[0], rental.Rental)


def test_should_call_get_rentals_by_user_id(query, db_rental):
    query.list_rentals_for_user.return_value = [db_rental]
    repo = RentalsRepository(query)
    actual_rentals = repo.get_rentals_by_user_id(db_rental.user_id)
    assert isinstance(actual_rentals[0], rental.Rental)


def test_should_call_get_by_id(query, db_rental):
    query.get_rental.return_value = db_rental
    repo = RentalsRepository(query)
    actual_rental = repo.get_by_id(db_rental.id)
    assert isinstance(actual_rental, rental.Rental)


def test_should_call_get_by_id_and_return_none(query):
    query.get_rental.return_value = None
    repo = RentalsRepository(query)
    actual_rental = repo.get_by_id("123")
    assert actual_rental is None


def test_should_call_complete_rental(query):
    query.complete_rental.return_value = None
    repo = RentalsRepository(query)

    local_rental = rental.Rental()
    local_rental.id = "R1"
    local_rental.user_id = "something"
    local_rental.asset_id = "asset_id"
    local_rental.created_at_location_id = "created_at_location_id"
    local_rental.created_at = "created_at"
    local_rental.expires_at = "expires_at"
    local_rental.eligible_asset_types = []
    local_rental.status = "status"
    local_rental.returned_at_location_id = "returned_at_location_id"
    local_rental.returned_at = "returned_at"

    repo.update(local_rental.id, local_rental.returned_at, local_rental.returned_at_location_id)
    print(query.complete_rental.call_args.args)
    assert query.complete_rental.call_args.args == (
        local_rental.id, "COMPLETED", local_rental.returned_at, local_rental.returned_at_location_id)
