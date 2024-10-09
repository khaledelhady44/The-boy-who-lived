import uuid

def generate_session_id() -> str:
    """Generates a unique session ID."""
    return str(uuid.uuid4())