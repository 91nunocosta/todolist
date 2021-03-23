from unittest.mock import patch


@patch.dict("os.environ", {"JWT_SECRET": "fake_secret"})
def test_authentication_functionality(clear_db, client):
    """
    Follows the following sequence:
    1. register a user
    2. login with that user
    3. create a task
    4. get list of task
    """
    account = {"username": "91nunocosta@gmail.com", "password": "unsecurepassword"}

    response = client.post("/accounts", json=account)

    assert response.status_code == 201

    response = client.post("/login", json=account)

    assert response.status_code == 200

    token = response.json["token"]

    response = client.post(
        "/tasks",
        json={
            "summary": "Do functional test of authorization.",
            "done": True,
            "position": 1,
        },
        headers={"Authorization": token},
    )

    assert response.status_code == 201

    response = client.get("/tasks", headers={"Authorization": token})

    total_items = response.json["_meta"]["total"]

    assert total_items == 1
