from enum import Enum

class ChatSender(Enum):
    """
    Enum class that defines the different types of chat message senders.

    Attributes:
    ----------
    USER : str
        Represents the user sending the message.
    
    SYSTEM : str
        Represents the system sending the message.
    """
    
    USER = "USER"
    SYSTEM = "SYSTEM"


class ChatSettings(Enum):
    """
    Enum class that defines chat-related settings and configurations.

    Attributes:
    ----------
    CHATS_COUNT_LIMIT : int
        The maximum number of chats a user can get.
    """
    
    CHATS_COUNT_LIMIT = 30
