from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId

from tests.helpers import items_without_meta


def test_update_task(client, db, user, token):
    db.tasks.drop()

    task = {
        "summary": "Test update!",
        "done": False,
        "position": 1,
        "_owner": user,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"tasks/{str(_id)}"
    data = {
        "done": True,
    }

    response = client.patch(url, data=data, headers={"Authorization": token})

    assert response.status_code == 200

    assert db.tasks.count() == 1

    updated_task = db.tasks.find_one({"_id": _id})
    assert updated_task is not None
    assert updated_task["done"] == True


def test_update_task_of_another_user(client, db, user, token, another_user):
    db.tasks.drop()

    task = {
        "summary": "Test update!",
        "done": False,
        "position": 1,
        "_owner": another_user,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"tasks/{str(_id)}"
    data = {
        "done": True,
    }

    response = client.patch(url, data=data, headers={"Authorization": token})

    assert response.status_code == 404

    # ensures nothing was changed
    assert db.tasks.find_one({"_id": _id})["done"] == False


def test_unauthorized_update_task(db, client):
    task = {
        "summary": "Test update!",
        "done": False,
    }

    _id = db.tasks.insert_one(task).inserted_id
    url = f"/tasks/{_id}"

    response = client.patch(url, json={})

    assert response.status_code == 401