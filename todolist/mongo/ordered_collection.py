"""
Provides functions for MongoDB for ordered collections.
"""
from typing import Any, Dict

import pymongo
from pymongo.collection import Collection


def add_position(
    collection: Collection,
    position: int,
) -> None:
    """
    Add a position to a MongoDB collection that is ordered by a position field.
    """
    if position <= 0:
        raise ValueError("Position should be greather than 0.")

    if position > get_last_position(collection) + 1:
        raise ValueError("Position should be contiguous to the existing position.")

    collection.update(
        {"position": {"$gte": position}}, {"$inc": {"position": 1}}, multi=True
    )


def get_last_position(collection: Collection) -> int:
    last_items = collection.find().sort([("position", pymongo.DESCENDING)]).limit(1)

    if last_items.count() < 1:
        return 0

    return last_items[0]["position"]