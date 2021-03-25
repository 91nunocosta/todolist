from typing import Any, Dict, Iterable

from flask import abort, current_app

from todolist.mongo.ordered_collection import (
    add_position,
    remove_position,
    update_position,
)


def tasks_collection():
    return current_app.data.driver.db.tasks


def add_task_positions(tasks: Iterable[Dict[str, Any]]) -> None:
    for task in tasks:
        try:
            add_position(
                tasks_collection(), task["position"], query={"_owner": task["_owner"]}
            )
        except ValueError:
            abort(422)


def remove_task_position(task: Dict[str, Any]) -> None:
    owner = tasks_collection().find_one({"_id": task["_id"]})["_owner"]
    remove_position(tasks_collection(), task["position"], query={"_owner": owner})


def update_task_positions(update, old_task) -> None:
    if "position" in update:
        try:
            owner = tasks_collection().find_one({"_id": old_task["_id"]})["_owner"]
            update_position(
                tasks_collection(),
                old_task["position"],
                update["position"],
                query={"_owner": owner},
            )
        except ValueError:
            abort(422)
