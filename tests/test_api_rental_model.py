from datetime import datetime
from unittest.mock import Mock

import pytz

from src.api.models.rental import Rental


def test_and_expires_at_is_nothing_get_expires_should_be_none():
    rental = Rental()
    rental.expires_at = None
    assert rental.get_expires_date() is None


def test_and_expires_at_is_date_string_get_expires_should_be_datetime():
    rental = Rental()
    now = datetime.now(pytz.utc)
    rental.expires_at = now.isoformat()
    assert rental.get_expires_date() == now


def test_and_expires_at_is_past_is_expired_should_be_true():
    expires_date = datetime.now(pytz.utc)
    expires_date = expires_date.replace(year=expires_date.year - 1)

    today = datetime.now(pytz.utc)

    rental = Rental()
    rental.expires_at = expires_date.isoformat()

    assert rental.is_expired(today) == True

def test_and_expires_at_is_future_is_expired_should_be_false():
    expires_date = datetime.now(pytz.utc)
    expires_date = expires_date.replace(year=expires_date.year + 1)

    today = datetime.now(pytz.utc)

    rental = Rental()
    rental.expires_at = expires_date.isoformat()

    assert rental.is_expired(today) == False


def test_status_is_none_is_completed_should_be_true():
    rental = Rental()
    rental.status = None
    assert rental.is_completed() == True


def test_status_is_not_completed_is_completed_should_be_false():
    rental = Rental()
    rental.status = "something"
    assert rental.is_completed() == False


def test_status_is_completed_completed_should_be_true():
    rental = Rental()
    rental.status = "COMPLETED"
    assert rental.is_completed() == True


def test_status_is_completed_false_and_is_expired_false_should_be_true():
    rental = Rental()
    rental.is_completed = Mock(name='is_completed', return_value=False)
    rental.is_expired = Mock(name='is_expired', return_value=False)
    assert rental.is_eligible_for_completion(datetime.now(pytz.utc)) == True


def test_status_is_completed_true_and_is_expired_false_should_be_false():
    rental = Rental()
    rental.is_completed = Mock(name='is_completed', return_value=True)
    rental.is_expired = Mock(name='is_expired', return_value=False)
    assert rental.is_eligible_for_completion(datetime.now(pytz.utc)) == False

def test_status_is_completed_true_and_is_expired_true_should_be_false():
    rental = Rental()
    rental.is_completed = Mock(name='is_completed', return_value=True)
    rental.is_expired = Mock(name='is_expired', return_value=True)
    assert rental.is_eligible_for_completion(datetime.now(pytz.utc)) == False

def test_status_is_completed_false_and_is_expired_true_should_be_false():
    rental = Rental()
    rental.is_completed = Mock(name='is_completed', return_value=False)
    rental.is_expired = Mock(name='is_expired', return_value=True)
    assert rental.is_eligible_for_completion(datetime.now(pytz.utc)) == False
