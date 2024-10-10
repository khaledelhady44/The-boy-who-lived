from pydantic import Field
from schemas.chat import BaseChat


class CreateChat(BaseChat):
    user_id: str = Field(...)
    