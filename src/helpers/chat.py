import uuid

def generate_session_id() -> str:
    """
    Generates a unique session ID using UUID.
    
    Returns:
    -------
    str
        A string representation of a randomly generated UUID, which can be used as a unique session ID.
    
    """

    return str(uuid.uuid4())