from models import MessageModel
from schemas.message import CreateMessage, MessageInDB
from helpers import generate_session_id
from enums import ChatSettings


class MessageController:
    def __init__(self, message_model:MessageModel):
        self.message_model = message_model

    async def create_message(self, message: CreateMessage):
        message_dict = message.dict()
        self.message_model.create_message(MessageInDB(**message_dict))


    async def get_full_chat(self, chat_id: str) -> list[MessageInDB]:
        return self.message_model.get_full_chat(chat_id)