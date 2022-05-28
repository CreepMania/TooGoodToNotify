from dataclasses import dataclass


@dataclass
class Favorite:
    display_name: str
    items_available: int
    in_sales_window: bool

    def __repr__(self):
        return f"'{self.display_name}' available! Qty: {self.items_available}"

    @property
    def is_available(self) -> bool:
        return self.items_available > 0 and self.in_sales_window
