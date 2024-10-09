from models import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.chat import MessageInDB
from enums import DataBaseEnum

class MessageModel(BaseDataModel):
    
    def __init__(self, db_client: AsyncIOMotorClient): # type: ignore

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.MESSAGE_COLLECTION.value]


    async def create_message(self, message: MessageInDB) -> None:
        message_dict = message.dict()
        await self.collection.insert_one(message_dict)

    async def get_full_chat(self, chat_id: str) -> list[MessageInDB]:
        return await self.collection.find({"chat_id": chat_id}).sort("timestamp", 1)