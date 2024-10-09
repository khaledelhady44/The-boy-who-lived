from pydantic import BaseModel, Field
from datetime import datetime

class BaseChat(BaseModel):
    user_id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

