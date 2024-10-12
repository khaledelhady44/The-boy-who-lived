from models import ChatModel
from schemas.chat import CreateChat, ChatInDB
from helpers import generate_session_id
from enums import ChatSettings


class ChatController:
    def __init__(self, chat_model:ChatModel):
        self.chat_model = chat_model

    async def create_chat(self, chat: CreateChat) -> ChatInDB:
        session_id = generate_session_id()
        chat_dict = chat.dict()
        chat_dict.update({"session_id": session_id})

        return await self.chat_model.create_chat(ChatInDB(**chat_dict))


    async def get_chat(self, session_id: str) -> ChatInDB:
        return await self.chat_model.get_chat(session_id)
    
    async def get_all_chats(self, user_id: str, limit: int = ChatSettings.CHATS_COUNT_LIMIT.value):
        return await self.chat_model.get_all_chats(user_id, limit)
    
    async def chat_exists(self, session_id: str, user_id: str) -> bool:
        return await self.chat_model.chat_exists(session_id, user_id)
    
    