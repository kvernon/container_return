import base64
from datetime import datetime

import pytz


class Event:
    timestamp: str
    location_id: str | None
    user_qr_data: str | None
    asset_qr_data: str | None

    def __decode__(self, value: str) -> str:
        return base64.b64decode(value).decode('utf-8')

    def __init__(self,
                 location_id: str = None,
                 user_qr_data: str = None,
                 asset_qr_data: str = None,
                 timestamp: str | None = None):
        if timestamp is None:
            self.timestamp = datetime.now(pytz.utc).isoformat()
        else:
            self.timestamp = timestamp

        self.location_id = location_id
        self.user_qr_data = user_qr_data
        self.asset_qr_data = asset_qr_data
        print(f"EVENT {self.timestamp}")

    def get_date(self) -> None | datetime:
        if self.timestamp is None:
            return None

        return datetime.fromisoformat(self.timestamp)

    def decoded_user_qr_data(self) -> None | str:
        if self.user_qr_data is None:
            return None

        return self.__decode__(self.user_qr_data)

    def decoded_asset_qr_data(self) -> None | str:
        if self.asset_qr_data is None:
            return None

        return self.__decode__(self.asset_qr_data)

    def is_valid(self) -> bool:
        return self.asset_qr_data is not None \
            and self.user_qr_data is not None \
            and self.location_id is not None \
            and self.timestamp is not None
