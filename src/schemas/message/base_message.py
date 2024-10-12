from pydantic import BaseModel, Field
from enums import ChatSender
from typing import Literal
from datetime import datetime

class BaseMessage(BaseModel):
    chat_id: str = Field(...)
    sender: Literal[ChatSender.SYSTEM.value, ChatSender.USER.value] # type: ignore
    message: str = Field(..., min_length = 1)
    timestamp : datetime = Field(default_factory=datetime.utcnow)

