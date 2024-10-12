from models import MessageModel
from schemas.message import CreateMessage, MessageInDB
class MessageController:
    def __init__(self, message_model:MessageModel):
        self.message_model = message_model

    async def create_message(self, message: CreateMessage) -> MessageInDB:
        message_dict = message.dict()
        return await self.message_model.create_message(MessageInDB(**message_dict))


    async def get_full_chat(self, chat_id: str) -> list[MessageInDB]:
        return await self.message_model.get_full_chat(chat_id)