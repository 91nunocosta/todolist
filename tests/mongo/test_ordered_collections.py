import pytest

from pymongo import MongoClient, ASCENDING

from todolist.mongo.ordered_collection import (
    check_position,
    get_last_position,
    add_position,
    remove_position,
    update_position,
)


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


def test_add_invalid_position(db_collection):
    db_collection.insert_one({"_id": 1, "position": 1})
    with pytest.raises(ValueError):
        add_position(db_collection, 0)


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


def test_add_position_to_the_middle_with_filter(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1, "option": 1},
        {"_id": 2, "position": 2, "option": 1},
        {"_id": 3, "position": 3, "option": 1},
        {"_id": 4, "position": 4, "option": 1},
        {"_id": 5, "position": 5, "option": 2},
    ]

    prepared_items = [
        {"_id": 1, "position": 1, "option": 1},
        {"_id": 2, "position": 2, "option": 1},
        {"_id": 3, "position": 4, "option": 1},
        {"_id": 4, "position": 5, "option": 1},
        {"_id": 5, "position": 5, "option": 2},
    ]

    db_collection.insert_many(items)

    add_position(db_collection, 3, query={"option": 1})

    assert db_items() == prepared_items


def test_remove_position_to_the_end(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
    ]
    db_collection.insert_many(items)

    remove_position(db_collection, 3)

    assert db_items() == items


def test_remove_invalid_position(db_collection):
    db_collection.insert_one({"_id": 1, "position": 1})

    with pytest.raises(ValueError):
        remove_position(db_collection, 0)


def test_remove_position_from_the_middle(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
    ]

    prepared_items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 2},
        {"_id": 4, "position": 3},
    ]

    db_collection.insert_many(items)

    remove_position(db_collection, 2)

    assert db_items() == prepared_items


def test_remove_position_from_the_middle_with_filter(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1, "option": 1},
        {"_id": 2, "position": 2, "option": 1},
        {"_id": 3, "position": 3, "option": 1},
        {"_id": 4, "position": 4, "option": 1},
        {"_id": 5, "position": 5, "option": 2},
    ]

    prepared_items = [
        {"_id": 1, "position": 1, "option": 1},
        {"_id": 2, "position": 2, "option": 1},
        {"_id": 3, "position": 2, "option": 1},
        {"_id": 4, "position": 3, "option": 1},
        {"_id": 5, "position": 5, "option": 2},
    ]

    db_collection.insert_many(items)

    remove_position(db_collection, 2, query={"option": 1})

    assert db_items() == prepared_items


def test_update_position_to_empty_collection(db_collection):
    with pytest.raises(ValueError):
        update_position(db_collection, 1, 1)


def test_update_invalid_new_position(db_collection):

    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
    ]

    db_collection.insert_many(items)

    with pytest.raises(ValueError):
        update_position(db_collection, 1, 5)


def test_update_invalid_old_position(db_collection):

    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
    ]

    db_collection.insert_many(items)

    with pytest.raises(ValueError):
        update_position(db_collection, 5, 1)


def test_update_to_same_position(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
    ]

    db_collection.insert_many(items)

    update_position(db_collection, 2, 2)

    assert db_items() == items


def test_move_down(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
        {"_id": 5, "position": 5},
        {"_id": 6, "position": 6},
    ]
    old_position = 2
    new_position = 5
    prepared_items = [
        {"_id": 1, "position": 1},
        # the position of target item is updated after update_position is executed
        # the function only updates items that aren't the target
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 2},
        {"_id": 4, "position": 3},
        {"_id": 5, "position": 4},
        {"_id": 6, "position": 6},
    ]

    db_collection.insert_many(items)

    update_position(db_collection, old_position, new_position)

    assert db_items() == prepared_items


def test_move_up(db_collection, db_items):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
        {"_id": 5, "position": 5},
        {"_id": 6, "position": 6},
    ]
    old_position = 5
    new_position = 2
    prepared_items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 3},
        {"_id": 3, "position": 4},
        {"_id": 4, "position": 5},
        # the position of target item is updated after update_position is executed
        # the function only updates items that aren't the target
        {"_id": 5, "position": 5},
        {"_id": 6, "position": 6},
    ]

    db_collection.insert_many(items)

    update_position(db_collection, old_position, new_position)

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


def test_get_last_position_with_filter(db_collection):
    items = [
        {"_id": 1, "position": 1, "option": 1},
        {"_id": 2, "position": 2, "option": 1},
        {"_id": 3, "position": 3, "option": 1},
        {"_id": 4, "position": 4, "option": 2},
    ]
    db_collection.insert_many(items)

    assert get_last_position(db_collection, query={"option": 1}) == 3


def test_check_non_positive_position(db_collection):
    with pytest.raises(ValueError):
        check_position(db_collection, 0)


def test_check_position_out_of_bounds(db_collection):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
    ]

    db_collection.insert_many(items)

    with pytest.raises(ValueError):
        check_position(db_collection, 5)


def test_check_valid_position(db_collection):
    items = [
        {"_id": 1, "position": 1},
        {"_id": 2, "position": 2},
        {"_id": 3, "position": 3},
        {"_id": 4, "position": 4},
    ]

    db_collection.insert_many(items)

    check_position(db_collection, 3)


def test_check_invalid_position_with_filter(db_collection):
    items = [
        {"_id": 1, "position": 1, "option": 1},
        {"_id": 2, "position": 2, "option": 1},
        {"_id": 3, "position": 3, "option": 1},
        {"_id": 4, "position": 4, "option": 2},
    ]

    db_collection.insert_many(items)

    with pytest.raises(ValueError):
        check_position(db_collection, 4, query={"option": 1})