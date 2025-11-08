from dataclasses import dataclass


@dataclass
class Response:
    code: int
    message: str
    data: dict
    timestamp: float