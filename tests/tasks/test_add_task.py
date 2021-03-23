from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId

from tests.helpers import items_without_meta


def test_add_task(client, db, user, token):
    db.tasks.drop()

    task = {
        "summary": "Test task creation!",
        "done": True,
        "position": 1,
    }

    response = client.post("tasks/", data=task, headers={"Authorization": token})

    assert response.status_code == 201

    assert db.tasks.count() == 1

    _id = ObjectId(response.json["_id"])

    added_task = db.tasks.find_one({"_id": _id})

    assert items_without_meta([added_task]) == items_without_meta([task])

    assert added_task["_owner"] == user


def test_unauthorized_add_task(client):

    response = client.post("/tasks", json={})

    assert response.status_code == 401