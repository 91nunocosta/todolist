def check_password(recieved_password: str, stored_password: str) -> bool:
    """
    Check if a recieved password matches the stored password.
    """
    return recieved_password == stored_password
