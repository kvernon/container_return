from src.api.models.event import Event
from src.encoders.map_to_event import map_to_event
import base64


def test_map_to_event_and_all_none():
    expected = Event()
    actual = map_to_event()
    assert expected.user_qr_data == actual.user_qr_data
    assert expected.asset_qr_data == actual.asset_qr_data
    assert expected.location_id == actual.location_id
    assert expected.timestamp != actual.timestamp


def test_map_to_event_and_none():
    user_id_encoded = "dHBnX3UwMDAx"
    user_id = "tpg_u0001"

    asset_id_encoded = "dHBnX2EwMDAwMQ=="
    asset_id = "tpg_a00001"

    location_id = "location_1"

    user_encoded = base64.b64encode(user_id.encode('utf-8')).decode('utf-8')
    asset_encoded = base64.b64encode(asset_id.encode('utf-8')).decode('utf-8')

    assert user_encoded == user_id_encoded
    assert asset_encoded == asset_id_encoded

    expected = Event(
        location_id,
        user_id_encoded,
        asset_id_encoded
    )

    actual = map_to_event(
        user_id,
        asset_id,
        location_id
    )

    assert expected.user_qr_data == actual.user_qr_data
    assert expected.asset_qr_data == actual.asset_qr_data
    assert expected.location_id == actual.location_id
    assert expected.timestamp != actual.timestamp
    assert actual.decoded_user_qr_data() == user_id;
    assert expected.decoded_asset_qr_data() == asset_id
