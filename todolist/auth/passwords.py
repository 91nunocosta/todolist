from bcrypt import checkpw, hashpw, gensalt


def check_password(recieved_password: str, stored_password: str) -> bool:
    """
    Check if a recieved password matches the stored password.
    """
    return checkpw(recieved_password.encode("utf-8"), stored_password)


def password_hash(password: str) -> str:
    """
    Returns the hash of a password.
    """
    return hashpw(password.encode("utf-8"), gensalt())
