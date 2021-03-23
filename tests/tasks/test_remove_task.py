from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId

from tests.helpers import items_without_meta


def test_remove_task(client, db, token):
    db.tasks.drop()

    task = {
            "summary": "Test listing tasks.",
            "done": True,
            "position": 1,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"tasks/{str(_id)}"

    response = client.delete(url, headers={"Authorization": token})
    assert response.status_code == 204

    assert db.tasks.count() == 1


def test_remove_task_of_another_user(client, db, user, token, another_user):
    db.tasks.drop()

    task = {
        "summary": "Test listing tasks.",
        "done": True,
        "position": 1,
        "_owner": another_user,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"tasks/{_id}"

    response = client.delete(url, headers={"Authorization": token})

    assert response.status_code == 204

    # ensures that nothing was removed
    assert db.tasks.count() == 1


def test_unauthorized_remove_task(db, user, client):
    task = {
        "summary": "Test delete!",
        "position": 1,
        "done": False,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"/tasks/{_id}"
    response = client.delete(url)

    assert response.status_code == 401
