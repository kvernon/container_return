from datetime import datetime
from typing import List

import pytz


class Rental:
    def __init__(self):
        pass

    id: str
    user_id: str
    asset_id: str
    created_at_location_id: str
    created_at: str
    expires_at: str
    status: str
    eligible_asset_types: List[str]
    returned_at_location_id: str
    returned_at: str

    def get_expires_date(self) -> None | datetime:
        if self.expires_at is None:
            return None

        return datetime.fromisoformat(self.expires_at)

    def is_expired(self, date: datetime) -> bool:
        if self.get_expires_date() is None:
            return True

        print("-------------------")
        print(date)
        print(self.get_expires_date())
        print("-------------------")
        return date.replace(tzinfo=pytz.utc) > self.get_expires_date()

    def is_completed(self):
        if self.status is None:
            return True
        return self.status == 'COMPLETED'

    def is_eligible_for_completion(self, date: datetime) -> bool:
        return not self.is_expired(date) and not self.is_completed()

    def to_dict(self):
        return self.__dict__
