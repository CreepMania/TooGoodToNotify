from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass
class PickupInterval:
    start: datetime
    end: datetime

    def __init__(self, start: str = None, end: str = None):
        self.start = None
        self.end = None

        # dates end with Z for UTC time, python does no parse iso dates that ends with Z :(
        # just remove the last character
        if start is not None:
            self.start = datetime.fromisoformat(start[:-1]).replace(tzinfo=timezone.utc)

        if end is not None:
            self.end = datetime.fromisoformat(end[:-1]).replace(tzinfo=timezone.utc)


@dataclass
class Favorite:
    __created_date = datetime.today()
    display_name: str
    items_available: int
    in_sales_window: bool
    item_id: int
    pickup_interval: Optional[PickupInterval]

    @property
    def is_available(self) -> bool:
        return self.items_available > 0 and self.in_sales_window

    @property
    def is_cache_expired(self) -> bool:
        return self.__created_date <= datetime.today() - timedelta(hours=2)
