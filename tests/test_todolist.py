from typing import Any, Dict
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


def test_add_taks(client, db):
    db.tasks.drop()

    task = {
        "summary": "Test todo item creation!",
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
