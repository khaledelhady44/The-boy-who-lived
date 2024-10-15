from models import MessageModel
from schemas.message import CreateMessage, MessageInDB

class MessageController:
    """
    Controller class for managing message-related operations.

    The MessageController handles interactions between the application logic and the
    `MessageModel` for creating and retrieving messages in the database.

    Attributes:
    ----------
    message_model : MessageModel
        An instance of the MessageModel used to interact with the message collection in the database.
    """
    
    def __init__(self, message_model: MessageModel):
        """
        Initializes the MessageController with the provided MessageModel instance.

        Args:
        ----
        message_model : MessageModel
            An instance of the MessageModel used to perform database operations.
        """
        self.message_model = message_model

    async def create_message(self, message: CreateMessage) -> MessageInDB:
        """
        Creates a new message and stores it in the database.

        Args:
        ----
        message : CreateMessage
            The data required to create a new message.

        Returns:
        -------
        MessageInDB
            The newly created message as it appears in the database, including its ID and timestamp.
        """
        message_dict = message.dict()  # Convert CreateMessage to dictionary
        return await self.message_model.create_message(MessageInDB(**message_dict))

    async def get_full_chat(self, chat_id: str) -> list[MessageInDB]:
        """
        Retrieves all messages from the database for a specific chat, ordered by timestamp.

        Args:
        ----
        chat_id : str
            The unique identifier of the chat whose messages are to be retrieved.

        Returns:
        -------
        list[MessageInDB]
            A list of messages for the specified chat, ordered by their timestamp.
        """
        return await self.message_model.get_full_chat(chat_id)
