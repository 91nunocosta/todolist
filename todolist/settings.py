# The next setting disables concurrency control (https://docs.python-eve.org/en/stable/features.html#concurrency).
# Concurrency control ensures that two clients requesting a change to a same item don't interfer with each other.
# The clients must prove it knows the latest version of the item.
# For that it needs to provide the correct etag (an hash).
# The etag is returned by the server on each operation over the item.

# I chose to disable this to make it easier to try out the API.
# In a real-life scenario I would't do so.
IF_MATCH = False

DOMAIN = {
    "tasks": {
        "resource_methods": ["GET", "POST"],
        "item_methods": ["PATCH", "DELETE"],
        "schema": {
            "summary": {
                "type": "string",
                "required": True,
            },
            "done": {
                "type": "boolean",
                "default": False,
            },
        },
    },
    "accounts": {
        "resource_methods": ["POST"],
        "schema": {
            "username": {
                "type": "string",
                "required": True,
            },
            "password": {
                "type": "string",
                "unique": True,
            },
        },
    },
}
