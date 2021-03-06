import pymongo
from bson.objectid import ObjectId

from tests.app.helpers import items_without_meta


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


def test_add_task_at_the_middle(client, db, user, token, another_user):
    db.tasks.drop()

    tasks = [
        {
            "summary": "Some previous task.",
            "position": 1,
            "done": True,
            "_owner": user,
        },
        {
            "summary": "Other task.",
            "position": 2,
            "done": True,
            "_owner": user,
        },
        {
            "summary": "Yet another task.",
            "position": 3,
            "done": False,
            "_owner": user,
        },
        {
            "summary": "Another user's task.",
            "position": 4,
            "done": False,
            "_owner": another_user,
        },
    ]
    new_task = {
        "summary": "Test adding task in the middle.",
        "position": 2,
        "done": True,
    }
    new_tasks = [
        {
            "summary": "Some previous task.",
            "position": 1,
            "done": True,
        },
        {
            "summary": "Test adding task in the middle.",
            "position": 2,
            "done": True,
        },
        {
            "summary": "Other task.",
            "position": 3,
            "done": True,
        },
        {
            "summary": "Yet another task.",
            "position": 4,
            "done": False,
        },
        {
            "summary": "Another user's task.",
            "position": 4,
            "done": False,
            "_owner": another_user,
        },
    ]

    db.tasks.insert_many(tasks)

    response = client.post("tasks/", data=new_task, headers={"Authorization": token})

    assert response.status_code == 201

    all_sorted_tasks = db.tasks.find().sort([("position", pymongo.ASCENDING)])

    assert items_without_meta(all_sorted_tasks) == items_without_meta(new_tasks)


def test_add_task_at_invalid_position(client, db, user, token):
    db.tasks.drop()

    task = {
        "summary": "Test task creation!",
        "done": True,
        "position": 2,
    }

    response = client.post("tasks/", data=task, headers={"Authorization": token})

    assert response.status_code == 422
