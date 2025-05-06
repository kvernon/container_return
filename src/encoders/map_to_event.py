import base64

from src.api.models.event import Event


def map_to_event(user_id: str | None = None,
                 asset_id: str | None = None,
                 location_id: str | None = None,
                 datetime: str | None = None) -> Event:
    user_encode = user_id
    asset_encode = asset_id

    if user_id is not None:
        user_encode = base64.b64encode(user_id.encode('utf-8')).decode('utf-8')

    if user_id is not None:
        asset_encode = base64.b64encode(asset_id.encode('utf-8')).decode('utf-8')

    return Event(location_id, user_encode, asset_encode, datetime)
