from models import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import MessageInDB
from enums import DataBaseEnum

class MessageModel(BaseDataModel):
    """
    MessageModel is a data access layer for managing message-related operations in the database.

    Attributes:
    ----------
    db_client : AsyncIOMotorClient
        The asynchronous MongoDB client used to interact with the database.

    collection : motor.AsyncIOMotorCollection
        The MongoDB collection used to store and retrieve message data.
    """
    
    def __init__(self, db_client: AsyncIOMotorClient):  # type: ignore
        """
        Initializes the MessageModel with the provided MongoDB client.

        Args:
        ----
        db_client : AsyncIOMotorClient
            An asynchronous MongoDB client to access the message collection.
        """

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.MESSAGE_COLLECTION.value]

    async def create_message(self, message: MessageInDB) -> MessageInDB:
        """
        Inserts a new message document into the database.

        Args:
        ----
        message : MessageInDB
            The message data to be inserted into the database.

        Returns:
        -------
        MessageInDB
            The inserted message object.
        """

        message_dict = message.dict()
        await self.collection.insert_one(message_dict)
        return message

    async def get_full_chat(self, chat_id: str) -> list[MessageInDB]:
        """
        Retrieves all messages associated with a given chat ID, ordered by the timestamp.

        Args:
        ----
        chat_id : str
            The unique identifier of the chat whose messages are to be retrieved.

        Returns:
        -------
        list[MessageInDB]
            A list of message objects representing the full chat conversation.
        """
        
        chat_cursor = self.collection.find({"chat_id": chat_id}).sort("timestamp", 1)
        messages = []
        async for message in chat_cursor:
            messages.append(MessageInDB(**message))
        
        return messages
