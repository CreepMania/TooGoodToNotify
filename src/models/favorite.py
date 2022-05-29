from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Favorite:
    __created_date = datetime.today()
    display_name: str
    items_available: int
    in_sales_window: bool
    item_id: int

    def __repr__(self):
        return f"{self.items_available} baskets available!"

    @property
    def is_available(self) -> bool:
        return self.items_available > 0 and self.in_sales_window

    @property
    def is_expired(self) -> bool:
        return self.__created_date <= datetime.today() - timedelta(hours=12)
