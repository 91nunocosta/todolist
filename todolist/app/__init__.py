from eve import Eve
from eve_swagger import get_swagger_blueprint

from todolist import __version__
from todolist.app.auth import JWTTokenAuth, login, replace_password_with_hash
from todolist.app.positions import (
    add_task_positions,
    remove_task_position,
    update_task_positions,
)
from todolist.app.settings import SETTINGS

swagger = get_swagger_blueprint()

app = Eve(auth=JWTTokenAuth, settings=SETTINGS)

app.on_insert_accounts += replace_password_with_hash

app.add_url_rule("/login", view_func=login, methods=["POST"])

app.on_insert_tasks += add_task_positions

app.on_delete_item_tasks += remove_task_position

app.on_update_tasks += update_task_positions

app.register_blueprint(swagger)

app.config["SWAGGER_INFO"] = {
    "title": "Todolist",
    "version": __version__,
    "description": "an API for managing tasks",
    "contact": {"name": "Nuno Costa"},
    "schemes": ["http"],
}
