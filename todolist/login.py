from typing import Any, Dict

from flask import current_app, request


def login():
    db = current_app.data.driver.db

    payload = request.get_json()
    username = payload["username"]
    password = payload["password"]

    account = db.accounts.find_one({"username": username})

    if account is not None and check_password(password, account["password"]):
        response = {"token": token(account)}
        return response, 200

    invalid_login_response = {
        "_status": "ERR",
        "_error": "Invalid username or password",
    }

    return invalid_login_response, 401


def token(account: Dict[str, Any]) -> str:
    """
    Returns a token that identifies a given user account.
    """
    pass


def check_password(recieved_password: str, stored_password: str) -> bool:
    """
    Check if a recieved password matches the stored password.
    """
    pass