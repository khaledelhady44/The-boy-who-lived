from schemas.message import BaseMessage
from pydantic import Field
from bson import ObjectId

class MessageInDB(BaseMessage):
    id: str = Field(default_facotry = lambda: str(ObjectId()))