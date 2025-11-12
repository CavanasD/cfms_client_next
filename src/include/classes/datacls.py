from dataclasses import dataclass


@dataclass
class User:
    username: str
    nickname: str
    created_at: float  # <- created_time
    last_login: float
    permissions: list[str]
    groups: list[str]