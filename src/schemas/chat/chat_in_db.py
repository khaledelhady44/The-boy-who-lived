from pydantic import Field
from schemas.chat import BaseChat
from bson import ObjectId

class ChatInDB(BaseChat):
    user_id: str = Field(...)
    session_id: str = Field(...)
    id: str = Field(default_factory = lambda: str(ObjectId()))