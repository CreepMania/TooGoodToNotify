from dataclasses import dataclass


@dataclass
class Credentials:
    access_token: str
    refresh_token: str
    user_id: str
