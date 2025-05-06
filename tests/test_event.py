import base64
from datetime import datetime

import pytz

from src.api.models.event import Event


def test_event_and_default():
    instance = Event()
    assert instance.timestamp is not None
    assert instance.location_id is None
    assert instance.user_qr_data is None
    assert instance.asset_qr_data is None
    assert instance.is_valid() is False


def test_event_and_populated():
    iso_format = datetime.now(pytz.utc).isoformat()
    instance = Event(
        location_id="location_id",
        user_qr_data="user_qr_data",
        asset_qr_data="asset_qr_data",
        timestamp=iso_format
    )
    assert instance.timestamp is iso_format
    assert instance.location_id is "location_id"
    assert instance.user_qr_data is "user_qr_data"
    assert instance.asset_qr_data is "asset_qr_data"
    assert instance.is_valid() is True


def test_should_extract_user_qr_data():
    value = "dHBnX3UwMDAx"
    # note decoded: 'tpg_u0001
    expected = base64.b64decode(value).decode('utf-8')
    instance = Event(user_qr_data=value)

    assert instance.decoded_user_qr_data() == expected


def test_should_not_extract_user_qr_data():
    instance = Event()

    assert instance.decoded_user_qr_data() is None



def test_should_render_date():
    instance = Event()

    assert instance.get_date() is not None


def test_should_not_render_date():
    instance = Event()
    instance.timestamp = None

    assert instance.get_date() is None


def test_should_not_extract_user_qr_data():
    instance = Event()

    assert instance.decoded_user_qr_data() is None


def test_should_extract_asset_qr_data():
    value = "dHBnX2EwMDAwMQ=="
    # note decoded: 'tpg_a00001
    expected = base64.b64decode(value).decode('utf-8')
    instance = Event(asset_qr_data=value)

    assert instance.decoded_asset_qr_data() == expected

def test_should_not_extract_asset_qr_data():
    instance = Event()

    assert instance.decoded_asset_qr_data() is None
