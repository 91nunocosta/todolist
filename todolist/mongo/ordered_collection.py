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

    if position > get_last_position(collection) + 1:
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
    check_position(collection, position)

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
    check_position(collection, position)

    collection.update(
        {"position": {"$gt": position}}, {"$inc": {"position": -1}}, multi=True
    )

def get_last_position(collection: Collection) -> int:
    last_items = collection.find().sort([("position", pymongo.DESCENDING)]).limit(1)

    if last_items.count() < 1:
        return 0

    return last_items[0]["position"]
