import pytest

from pymongo import MongoClient, ASCENDING

from todolist.mongo.ordered_collection import get_last_position, add_position


@pytest.fixture
def db_collection():
    client = MongoClient()
    db = client["my_db"]
    collection = db["my_collection"]
    collection.drop()
    return collection


@pytest.fixture
def db_items(db_collection):
    return lambda: list(db_collection.find().sort([("position", ASCENDING)]))


def test_add_position_to_empty_collection(db_collection):
    add_position(db_collection, 1)

    assert db_collection.count() == 0


def test_add_position_to_the_end(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
    ]
    db_collection.insert_many(items)

    add_position(db_collection, 4)

    assert db_items() == items


def test_add_non_positive_position(db_collection):
    with pytest.raises(ValueError):
        add_position(db_collection, 0)


def test_add_non_contiguous_position(db_collection):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
    ]

    db_collection.insert_many(items)

    with pytest.raises(ValueError):
        add_position(db_collection, 6)


def test_add_position_to_the_middle(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
    ]

    prepared_items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 4},
        {"_id": 4, "position": 5},
    ]

    db_collection.insert_many(items)

    add_position(db_collection, 3)

    assert db_items() == prepared_items


def test_get_last_position_of_empty_collection(db_collection):
    assert get_last_position(db_collection) == 0


def test_get_last_position(db_collection):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
    ]
    db_collection.insert_many(items)

    assert get_last_position(db_collection) == 4