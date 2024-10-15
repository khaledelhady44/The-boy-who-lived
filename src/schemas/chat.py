from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class BaseChat(BaseModel):
    """
    BaseChat is a Pydantic model that represents the basic attributes of a chat session.

    Attributes:
    ----------
    name : str
        The name of the chat or conversation.

    user_id : str
        The unique identifier of the user who initiated the chat.

    created_at : datetime
        The timestamp of when the chat was created. Defaults to the current UTC time.

    updated_at : datetime
        The timestamp of the last time the chat was updated. Defaults to the current UTC time.
    """

    name: str = Field(..., min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CreateChat(BaseChat):
    """
    CreateChat is a Pydantic model that inherits from BaseChat and is used to create a new chat session.

    Inherits all attributes from BaseChat.
    """
    pass


class ChatInDB(BaseChat):
    """
    ChatInDB is a Pydantic model that represents a chat session stored in the database.

    Attributes:
    ----------
    id : str
        The unique identifier for the chat session in the database. Defaults to a newly generated ObjectId.
    
    session_id : str
        The unique session identifier that links related chat messages or conversations.
    
    Inherits all attributes from BaseChat.
    """

    id: str = Field(default_factory=lambda: str(ObjectId()))
    session_id: str = Field(...)
    user_id: str = Field(...)
