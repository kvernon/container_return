from unittest.mock import Mock

import pytest

from repositories.users_repository import UsersRepository
from jojanga_queries import users
from jojanga_queries.users import User


@pytest.fixture()
def query():
    the_users = users
    the_users.get_user = Mock(name="get_user")
    yield the_users


@pytest.fixture()
def db_user():
    the_user = User(
        id="howdy-id",
        name="howdy-username"
    )

    yield the_user


def test_should_call_get_user_by_id(query, db_user):
    query.get_user.return_value = db_user
    repo = UsersRepository(query)
    actual = repo.get_user_by_id(db_user.id)
    assert actual is not None


def test_should_call_get_user_by_id_should_be_none(query):
    query.get_user.return_value = None
    repo = UsersRepository(query)
    actual = repo.get_user_by_id("howdy-id")
    assert actual is None
