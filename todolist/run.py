from eve import Eve

from eve.auth import TokenAuth

from todolist.auth.tokens import check_token
from todolist.login import login


class JWTTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return check_token(token)


app = Eve(auth=JWTTokenAuth)
app.add_url_rule("/login", view_func=login, methods=["POST"])

if __name__ == "__main__":
    app.run()