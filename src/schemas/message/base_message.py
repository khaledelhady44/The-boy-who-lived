from pydantic import BaseModel, Field
from enums import ChatSender
from datetime import datetime

class BaseMessgage(BaseModel):
    chat_id: str = Field(...)
    sender: ChatSender
    message: str = Field(..., min_length = 1)
    timestamp = datetime = Field(default_factory=datetime.utcnow)
