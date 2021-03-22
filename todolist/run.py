from typing import Any, Dict, Iterable

from eve import Eve

from eve.auth import TokenAuth

from todolist.auth.tokens import check_token
from todolist.auth.passwords import password_hash
from todolist.login import login


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

app.add_url_rule("/login", view_func=login, methods=["POST"])

app.on_insert_accounts += replace_password_with_hash

if __name__ == "__main__":
    app.run()