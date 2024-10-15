from pydantic import BaseModel, Field
from enums import ChatSender
from typing import Literal, Optional
from datetime import datetime
from bson import ObjectId

class BaseMessage(BaseModel):
    """
    BaseMessage is a Pydantic model representing the basic structure of a chat message.

    Attributes:
    ----------
    chat_id : str
        The unique identifier of the chat to which this message belongs.
    
    sender : Literal
        The sender of the message. It can either be "system" or "user" based on the `ChatSender` enum.
    
    message : str
        The content of the message. It must contain at least one character.
    
    timestamp : datetime
        The time at which the message was sent. Defaults to the current UTC time.
    """

    chat_id: str = Field(...)
    sender: Literal[ChatSender.SYSTEM.value, ChatSender.USER.value]  # type: ignore
    message: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CreateMessage(BaseMessage):
    """
    CreateMessage is a Pydantic model used for creating a new chat message.

    Inherits all attributes from BaseMessage.
    """
    pass


class MessageInDB(BaseMessage):
    """
    MessageInDB is a Pydantic model representing a chat message stored in the database.

    Attributes:
    ----------
    id : Optional[str]
        The unique identifier for the message in the database. Defaults to a newly generated ObjectId.

    Inherits all attributes from BaseMessage.
    """
    
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
