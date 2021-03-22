from typing import Any, Dict
import os

from datetime import datetime

from jwt import encode


SECRET_ENV_VARIABLE = "JWT_SECRET"


def generate_token(account: Dict[str, Any]) -> str:
    """
    Returns a token that identifies a given user account.
    """
    payload = {
        "sub": account["username"],
        "iat": datetime.utcnow(),
    }
    secret = os.environ[SECRET_ENV_VARIABLE]
    return encode(payload, secret)


class InvalidToken(Exception):
    pass


class ExpiredToken(Exception):
    pass


def check_token(token: str) -> Dict[str, Any]:
    """
    Decodes a token and verifies it authenticity.

    Returns the data of the token.

    Raises ValueError if the token is empty.

    Raises InvalidToken if the token is not authentic. There are two possibilities:
    - the token was not issued by a trusted authentication server
    - the token was tempered.

    Raises Expired token if the token is expired.
    """
    if not token:
        raise ValueError()