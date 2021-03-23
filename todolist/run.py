from typing import Any, Dict, Iterable
from flask import abort
from eve import Eve

from eve.auth import TokenAuth

from todolist.auth.tokens import check_token
from todolist.auth.passwords import password_hash
from todolist.login import login
from todolist.mongo.ordered_collection import (
    add_position,
    remove_position,
    update_position,
)


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
        try:
            add_position(tasks_collection(), task["position"])
        except ValueError:
            abort(422)


def remove_task_position(task: Dict[str, Any]) -> None:
    remove_position(tasks_collection(), task["position"])


def update_positions(update, old_task) -> None:
    if "position" in update:
        try:
            update_position(
                tasks_collection(), old_task["position"], update["position"]
            )
        except ValueError:
            abort(422)


app.add_url_rule("/login", view_func=login, methods=["POST"])

app.on_insert_accounts += replace_password_with_hash

app.on_insert_tasks += add_positions

app.on_delete_item_tasks += remove_task_position

app.on_update_tasks += update_positions

if __name__ == "__main__":
    app.run()