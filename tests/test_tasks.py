from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId

from tests.helpers import items_without_meta


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

    assert items_without_meta([added_task]) == items_without_meta([task])


def test_update_task(client, db):
    db.tasks.drop()

    task = {
        "summary": "Test update!",
        "done": False,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"tasks/{str(_id)}"
    print(url)
    data = {
        "done": True,
    }

    response = client.patch(url, data=data)

    print(response.json)

    assert response.status_code == 200

    assert db.tasks.count() == 1

    updated_task = db.tasks.find_one({"_id": _id})
    assert updated_task is not None
    assert updated_task["done"] == True


def test_remove_task(client, db):
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
    ]

    result = db.tasks.insert_many(tasks)
    some_id = str(result.inserted_ids[0])

    url = f"tasks/{some_id}"

    response = client.delete(url)
    assert response.status_code == 204

    assert db.tasks.count()
