"""
Provides functions for MongoDB for ordered collections.
"""
from typing import Any, Dict

import pymongo
from pymongo.collection import Collection


def check_position(collection: Collection, position: int) -> None:
    """
    Check if a position is valid in a given collections.

    A position is valid iff:
        1. it is greather than 0; and
        2. no greather than the position succeeding the largest position.

    Raises ValueError if any of the above conditions is violated.
    """
    if position <= 0:
        raise ValueError("Position should be greather than 0.")

    if position > get_last_position(collection):
        raise ValueError("Position should be contiguous to the existing position.")


def add_position(
    collection: Collection,
    position: int,
) -> None:
    """
    Add a position to a MongoDB collection that is ordered by a position field.

    All items after the given position are shifted to the right.
    By other words, the positions of those items are incremented by one.
    No item is actually added.
    """
    if collection.count() < 1:
        return

    if position <= 0:
        raise ValueError("Position should be greather than 0.")

    if position > get_last_position(collection) + 1:
        raise ValueError("Position should be contiguous to the existing position.")

    collection.update(
        {"position": {"$gte": position}}, {"$inc": {"position": 1}}, multi=True
    )


def remove_position(
    collection: Collection,
    position: int,
):
    """
    Remove a position from a MongoDB collection that is ordered by a position field.

    All items after the position are shifted (decremented by one) to the left.
    By other words, the positions of those items are decremented by one.
    """
    if collection.count() < 1:
        return

    check_position(collection, position)

    collection.update(
        {"position": {"$gt": position}}, {"$inc": {"position": -1}}, multi=True
    )


def update_position(
    collection: Collection, old_position: int, new_position: int
) -> None:
    """
    Updates a position in a MongoDB collection that is ordered by a position field.
    """
    check_position(collection, old_position)
    check_position(collection, new_position)

    if collection.count() < 1:
        raise ValueError("The collection to update is empty.")

    if old_position < new_position:
        collection.update_many(
            {"position": {"$gt": old_position, "$lte": new_position}},
            {"$inc": {"position": -1}},
        )
    if old_position > new_position:
        collection.update_many(
            {"position": {"$gte": new_position, "$lt": old_position}},
            {"$inc": {"position": 1}},
        )


def get_last_position(collection: Collection) -> int:
    last_items = collection.find().sort([("position", pymongo.DESCENDING)]).limit(1)

    if last_items.count() < 1:
        return 0

    return last_items[0]["position"]
