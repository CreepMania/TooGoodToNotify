from dataclasses import dataclass


@dataclass
class Credentials:
    access_token: str
    refresh_token: str
    user_id: str

    @property
    def is_valid(self) -> bool:
        return self.access_token not in [None, ""] \
               and self.refresh_token not in [None, ""] \
               and self.user_id is not None
