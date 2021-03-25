import pymongo

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
    assert updated_task["done"]


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
    assert not db.tasks.find_one({"_id": _id})["done"]


def test_unauthorized_update_task(db, client):
    task = {
        "summary": "Test update!",
        "done": False,
    }

    _id = db.tasks.insert_one(task).inserted_id
    url = f"/tasks/{_id}"

    response = client.patch(url, json={})

    assert response.status_code == 401


def test_update_task_in_the_middle(client, db, user, token, another_user):
    db.tasks.drop()

    tasks = [
        {
            "summary": "Task 1",
            "done": False,
            "position": 1,
            "_owner": user,
        },
        {
            "summary": "Task 2",
            "done": False,
            "position": 2,
            "_owner": user,
        },
        {
            "summary": "Another user's task",
            "done": False,
            "position": 2,
            "_owner": another_user,
        },
        {
            "summary": "Task 3",
            "done": False,
            "position": 3,
            "_owner": user,
        },
    ]

    new_tasks = [
        {
            "summary": "Task 3",
            "done": False,
            "position": 1,
            "_owner": user,
        },
        {
            "summary": "Task 1",
            "done": False,
            "position": 2,
            "_owner": user,
        },
        {
            "summary": "Another user's task",
            "done": False,
            "position": 2,
            "_owner": another_user,
        },
        {
            "summary": "Task 2",
            "done": False,
            "position": 3,
            "_owner": user,
        },
    ]

    db.tasks.insert_one(tasks[0])
    db.tasks.insert_one(tasks[1])
    db.tasks.insert_one(tasks[2])
    _id = db.tasks.insert_one(tasks[3]).inserted_id

    url = f"tasks/{str(_id)}"
    data = {
        "position": "1",
    }

    response = client.patch(url, data=data, headers={"Authorization": token})

    assert response.status_code == 200

    all_sorted_tasks = db.tasks.find().sort([("position", pymongo.ASCENDING)])

    assert items_without_meta(all_sorted_tasks) == items_without_meta(new_tasks)


def test_update_task_with_invalid_position(client, db, user, token):
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
        "position": 3,
    }

    response = client.patch(url, data=data, headers={"Authorization": token})

    assert response.status_code == 422
