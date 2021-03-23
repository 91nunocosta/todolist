from typing import Any, Dict, Iterable

from eve import Eve

from eve.auth import TokenAuth

from todolist.auth.tokens import check_token
from todolist.auth.passwords import password_hash
from todolist.login import login
from todolist.mongo.ordered_collection import add_position


class JWTTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        token_payload = check_token(token)
        username = token_payload["sub"]
        self.set_request_auth_value(username)
        return token_payload is not None


def replace_password_with_hash(items: Iterable[Dict[str, Any]]) -> None:
    """
    Replaces the password in a account item by a corresponding hash.
    """
    for account_item in items:
        password = account_item["password"]
        account_item["password"] = password_hash(password)


app = Eve(auth=JWTTokenAuth)


def tasks_collection():
    return app.data.driver.db.tasks


def add_positions(tasks: Iterable[Dict[str, Any]]) -> None:
    for task in tasks:
        add_position(tasks_collection(), task["position"])


app.add_url_rule("/login", view_func=login, methods=["POST"])

app.on_insert_accounts += replace_password_with_hash

app.on_insert_tasks += add_positions

if __name__ == "__main__":
    app.run()