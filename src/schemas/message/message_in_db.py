from schemas.message import BaseMessage
from pydantic import Field
from bson import ObjectId
from typing import Optional

class MessageInDB(BaseMessage):
    id: Optional[str] = Field(default_factory = lambda: str(ObjectId()))
                    