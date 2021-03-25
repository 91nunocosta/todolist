from flask import current_app, request

from todolist.auth.passwords import check_password
from todolist.auth.tokens import generate_token


def login():
    db = current_app.data.driver.db

    payload = request.get_json()
    username = payload["username"]
    password = payload["password"]

    account = db.accounts.find_one({"username": username})

    if account is not None and check_password(password, account["password"]):
        response = {"token": generate_token(username)}
        return response, 200

    invalid_login_response = {
        "_status": "ERR",
        "_error": "Invalid username or password",
    }

    return invalid_login_response, 401
