from enum import Enum

class ChatSender(Enum):
    USER = "user"
    SYSTEM = "SYSTEM"

class ChatSettings(Enum):
    CHATS_COUNT_LIMIT = 5