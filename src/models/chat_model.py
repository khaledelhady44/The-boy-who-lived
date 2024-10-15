from models import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import ChatInDB
from enums import DataBaseEnum
from typing import Optional

class ChatModel(BaseDataModel):
    """
    ChatModel is a data access layer for managing chat-related operations in the database.

    Attributes:
    ----------
    db_client : AsyncIOMotorClient
        The asynchronous MongoDB client used to interact with the database.

    collection : motor.AsyncIOMotorCollection
        The MongoDB collection used to store and retrieve chat data.
    """
    
    def __init__(self, db_client: AsyncIOMotorClient):  # type: ignore
        """
        Initializes the ChatModel with the provided MongoDB client.

        Args:
        ----
        db_client : AsyncIOMotorClient
            An asynchronous MongoDB client to access the chat collection.
        """

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.CHAT_COLLECTION.value]

    async def create_chat(self, chat: ChatInDB) -> ChatInDB:
        """
        Inserts a new chat document into the database.

        Args:
        ----
        chat : ChatInDB
            The chat data to be inserted into the database.

        Returns:
        -------
        ChatInDB
            The inserted chat object.
        """

        chat_dict = chat.dict()
        await self.collection.insert_one(chat_dict)
        return chat

    async def get_chat(self, session_id: str) -> Optional[ChatInDB]:
        """
        Retrieves a chat document from the database by session ID.

        Args:
        ----
        session_id : str
            The unique session ID of the chat.

        Returns:
        -------
        Optional[ChatInDB]
            The chat object if found, otherwise None.
        """

        chat_data = await self.collection.find_one({"session_id": session_id})
        if chat_data:
            return ChatInDB(**chat_data)
        
        return None

    async def get_all_chats(self, user_id: str, limit: int) -> Optional[list[ChatInDB]]:
        """
        Retrieves all chat documents for a given user, up to a specified limit.

        Args:
        ----
        user_id : str
            The unique ID of the user who owns the chats.

        limit : int
            The maximum number of chat documents to retrieve.

        Returns:
        -------
        Optional[list[ChatInDB]]
            A list of chat objects, or None if no chats are found.
        """

        chats_cursor = self.collection.find({"user_id": user_id}).limit(limit)
        
        chats = []
        async for chat in chats_cursor:
            chats.append(ChatInDB(**chat))

        return chats

    async def chat_exists(self, session_id: str, user_id: str) -> bool:
        """
        Checks if a chat with the specified session ID and user ID exists in the database.

        Args:
        ----
        session_id : str
            The unique session ID of the chat.

        user_id : str
            The unique ID of the user who owns the chat.

        Returns:
        -------
        bool
            True if the chat exists, otherwise False.
        """
        
        chat_data = await self.collection.find_one({"session_id": session_id, "user_id": user_id})
        return chat_data is not None
