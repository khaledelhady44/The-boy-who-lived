from enum import Enum

class DataBaseEnum(Enum):
    """
    Enum class that defines the MongoDB collection names used in the application.

    Attributes:
    ----------
    USER_COLLECTION : str
        The name of the collection that stores user data.
    
    CHAT_COLLECTION : str
        The name of the collection that stores chat data.
    
    MESSAGE_COLLECTION : str
        The name of the collection that stores message data.
    """
    
    USER_COLLECTION = "users"
    CHAT_COLLECTION = "chat"
    MESSAGE_COLLECTION = "message"
