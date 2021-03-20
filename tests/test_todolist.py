from typing import Any, Dict, List, Set
import pytest
from bson.objectid import ObjectId

from todolist import __version__

from todolist.run import app


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def db():
    with app.app_context():
        return app.data.driver.db


def test_get_root(client):
    response = client.get("/")

    assert response.status_code == 200


def test_list_all_tasks(client, db):
    db.tasks.drop()

    tasks = [
        {
            "summary": "Test listing tasks.",
            "done": True,
        },
        {
            "summary": "Configure Kubernetes.",
            "done": False,
        },
        {
            "summary": "Configure helm.",
            "done": False,
        },
    ]

    db.tasks.insert_many(tasks)

    response = client.get("tasks/")

    assert response.status_code == 200

    assert items_without_meta(response.json["_items"]) == items_without_meta(tasks)


def test_add_taks(client, db):
    db.tasks.drop()

    task = {
        "summary": "Test task creation!",
        "done": True,
    }

    response = client.post("tasks/", data=task)

    assert response.status_code == 201

    assert db.tasks.count() == 1

    _id = ObjectId(response.json["_id"])

    added_task = db.tasks.find_one({"_id": _id})

    assert match(added_task, task)


def match(db_dict: Dict[str, Any], request_dict: Dict[str, Any]) -> bool:
    """`
    Returns true iff all key-value pairs of request_dict are in db_dict.

    By other words, `db_dict` is the expected MonogoDB representation of the json request body `request_dict.
    """
    return all(db_dict[key] == request_dict[key] for key in request_dict)


def items_without_meta(items: Dict[str, Any]) -> List[Dict[str, Any]]:
    """`
    Returns all items contained in a response, excluding all metadata fields.
    """

    def item_without_meta(item_with_meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: value
            for key, value in item_with_meta.items()
            if not key.startswith("_")
        }

    return [item_without_meta(i) for i in items]