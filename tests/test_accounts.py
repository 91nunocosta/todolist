from tests.helpers import items_without_meta


def test_add_account(db, client):
    db.accounts.drop()

    account = {"username": "91nunocosta@gmail.com", "password": "unsecurepassword"}

    response = client.post("/accounts", json=account)

    assert response.status_code == 201

    added_account = db.accounts.find_one()
    assert items_without_meta([added_account]) == items_without_meta([account])