from unittest.mock import Mock

import pytest

from repositories.assets_repository import AssetsRepository
from repositories.users_repository import UsersRepository
from src.api.main import create_app
from repositories.rentals_repository import RentalsRepository
from src.api.models.rental import Rental


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app
    app.container.unwire()

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
def client(app):
    yield app.test_client()

@pytest.fixture
def rentals_repo_mock():
    mock = RentalsRepository(None)
    mock.get_rentals_by_user_id = Mock(name="get_rentals_by_user_id")
    mock.get_by_id = Mock(name="get_by_id")
    mock.get_in_progress_rentals_for_user = Mock(name="get_in_progress_rentals_for_user")
    yield mock

@pytest.fixture
def rental():
    rental_setup = Rental()
    rental_setup.user_id = 'user_id'
    rental_setup.id = "id"
    rental_setup.asset_id = "asset_id"
    rental_setup.created_at_location_id = "created_at_location_id"
    rental_setup.created_at = "created_at"
    rental_setup.expires_at = "expires_at"
    rental_setup.status = "status"
    rental_setup.eligible_asset_types = []
    rental_setup.returned_at_location_id = "returned_at_location_id"
    rental_setup.returned_at = "returned_at"

    yield rental_setup