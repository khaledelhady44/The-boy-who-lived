from models import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.chat import ChatInDB
from enums import DataBaseEnum
from typing import Optional

class ChatModel(BaseDataModel):
    
    def __init__(self, db_client: AsyncIOMotorClient): # type: ignore
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.CHAT_COLLECTION.value]


    async def create_chat(self, chat: ChatInDB) -> ChatInDB:
        chat_dict = chat.dict()
        await self.collection.insert_one(chat_dict)
        return chat

    async def get_chat(self, session_id: str) -> Optional[ChatInDB]:

        chat_data = await self.collection.find_one({"session_id": session_id})
        if chat_data:
            return ChatInDB(**chat_data)
        
        return None

    async def get_all_chats(self, user_id: str, limit: int) -> Optional[list[ChatInDB]]:
        chats_cursor = self.collection.find({"user_id": user_id}).limit(limit)
        
        chats = []
        async for chat in chats_cursor:
            chats.append(ChatInDB(**chat))

        return chats
    
    async def chat_exists(self, session_id: str, user_id: str) -> bool:

        chat_data = await self.collection.find_one({"session_id": session_id, "user_id": user_id})
        return chat_data is not None
    
    