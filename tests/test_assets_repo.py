from unittest.mock import Mock

import pytest

from repositories.assets_repository import AssetsRepository
from jojanga_queries import assets
from jojanga_queries.assets import Asset


@pytest.fixture()
def query():
    the_assets = assets
    the_assets.get_asset = Mock(name="get_asset")
    yield the_assets


@pytest.fixture()
def db_asset():
    the_asset = Asset(
        id="asset-id",
        asset_type="1"
    )

    yield the_asset


def test_should_call_get_asset_by_id(query, db_asset):
    query.get_asset.return_value = db_asset
    repo = AssetsRepository(query)
    actual = repo.get_asset_by_id(db_asset.id)
    assert actual is not None


def test_should_call_get_asset_by_id_should_be_none(query):
    query.get_asset.return_value = None
    repo = AssetsRepository(query)
    actual = repo.get_asset_by_id("howdy-id")
    assert actual is None
