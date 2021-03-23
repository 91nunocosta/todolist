from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId
import pymongo

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


def test_remove_task_from_the_middle(client, db, token):
    db.tasks.drop()

    tasks = [
        {
            "summary": "Test listing tasks.",
            "done": True,
            "position": 1,
        },
        {
            "summary": "Configure Kubernetes.",
            "position": 2,
            "done": False,
        },
        {
            "summary": "Test listing something else.",
            "done": True,
            "position": 3,
        },
    ]
    new_tasks = [
        {
            "summary": "Test listing tasks.",
            "done": True,
            "position": 1,
        },
        {
            "summary": "Test listing something else.",
            "done": True,
            "position": 2,
        },
    ]

    def create_task(task) -> str:
        response = client.post("/tasks/", json=task, headers={"Authorization": token})
        return response.json["_id"]

    create_task(tasks[0])
    _id = create_task(tasks[1])
    create_task(tasks[2])

    url = f"tasks/{_id}"

    response = client.delete(url, headers={"Authorization": token})
    assert response.status_code == 204

    assert db.tasks.count() == 2

    all_sorted_tasks = db.tasks.find().sort([("position", pymongo.ASCENDING)])

    assert items_without_meta(all_sorted_tasks) == items_without_meta(new_tasks)
