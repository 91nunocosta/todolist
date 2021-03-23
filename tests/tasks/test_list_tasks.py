from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId

from tests.helpers import items_without_meta


def test_list_tasks(db, client, user, token, another_user):
    db.tasks.drop()

    tasks = [
        {
            "summary": "Test listing tasks.",
            "done": True,
            "position": 1,
            "_owner": user,
        },
        {
            "summary": "Configure Kubernetes.",
            "done": False,
            "position": 2,
            "_owner": user,
        },
        {"summary": "Configure helm.", "done": False, "position": 3, "_owner": user},
    ]

    db.tasks.insert_many(tasks)

    db.tasks.insert_one(
        {
            "summary": "Check that he can't see this task, because I'm another user.",
            "done": True,
            "position": 4,
            "_owner": another_user,
        }
    )

    response = client.get("tasks/", headers={"Authorization": token})

    assert response.status_code == 200

    assert items_without_meta(response.json["_items"]) == items_without_meta(tasks)


def test_unauthorized_list_tasks(client):

    response = client.get("/tasks")

    assert response.status_code == 401
