from typing import Any, Dict, Iterable, List, Set
from bson.objectid import ObjectId

from tests.helpers import items_without_meta


def test_list_tasks(db, client, user, token, another_user):
    db.tasks.drop()

    tasks = [
        {
            "summary": "Test listing tasks.",
            "done": True,
            "_owner": user,
        },
        {"summary": "Configure Kubernetes.", "done": False, "_owner": user},
        {"summary": "Configure helm.", "done": False, "_owner": user},
    ]

    db.tasks.insert_many(tasks)

    db.tasks.insert_one(
        {
            "summary": "Check that he can't see this task, because I'm another user.",
            "done": True,
            "_owner": another_user,
        }
    )

    response = client.get("tasks/", headers={"Authorization": token})

    assert response.status_code == 200

    assert items_without_meta(response.json["_items"]) == items_without_meta(tasks)


def test_unauthorized_list_tasks(client):

    response = client.get("/tasks")

    assert response.status_code == 401


def test_add_task(client, db, user, token):
    db.tasks.drop()

    task = {
        "summary": "Test task creation!",
        "done": True,
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


def test_update_task(client, db, user, token):
    db.tasks.drop()

    task = {
        "summary": "Test update!",
        "done": False,
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


def test_remove_task(client, db, token):
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

    response = client.delete(url, headers={"Authorization": token})
    assert response.status_code == 204

    assert db.tasks.count()


def test_remove_task_of_another_user(client, db, user, token, another_user):
    db.tasks.drop()

    task = {
        "summary": "Test listing tasks.",
        "done": True,
        "_owner": another_user,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"tasks/{_id}"

    response = client.delete(url, headers={"Authorization": token})

    assert response.status_code == 204

    # ensures that nothing was removed
    assert db.tasks.count() == 1


def test_unauthorized_remove_task(db, client):
    task = {
        "summary": "Test delete!",
        "done": False,
    }

    _id = db.tasks.insert_one(task).inserted_id

    url = f"/tasks/{_id}"
    response = client.delete(url)

    assert response.status_code == 401
