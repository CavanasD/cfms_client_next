import secrets
import string

__all__ = ["generate_random_password"]


def generate_random_password() -> str:
    password = "".join(
        secrets.choice(string.ascii_letters + string.digits + string.punctuation)
        for _ in range(16)
    )
    return password
