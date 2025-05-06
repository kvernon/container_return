from src.api.models.rental import Rental
from src.api.models.rental_filters import get_first_match


def test_and_collection_is_empty_should_return_none():
    assert get_first_match([], "something") is None

def test_and_collection_is_populated_with_empty_eligible_should_return_none():
    rental = Rental()
    rental.eligible_asset_types = []
    assert get_first_match([rental], "something") is None

def test_and_collection_is_populated_with_no_match_should_return_none():
    rental = Rental()
    rental.eligible_asset_types = ["foo"]
    assert get_first_match([rental], "something") is None

def test_and_collection_is_populated_with_match_should_return_none():
    rental = Rental()
    matched_value = "something"
    rental.eligible_asset_types = [matched_value]
    assert get_first_match([rental], matched_value) is rental