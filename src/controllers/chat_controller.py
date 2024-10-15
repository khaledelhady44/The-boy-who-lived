from models import ChatModel
from schemas.chat import CreateChat, ChatInDB
from helpers import generate_session_id
from enums import ChatSettings

class ChatController:
    """
    Controller class for managing chat-related operations.

    The ChatController handles the interaction between the application logic and the
    `ChatModel` for creating, retrieving, and managing chats in the database.

    Attributes:
    ----------
    chat_model : ChatModel
        An instance of the ChatModel used to interact with the chat collection in the database.
    """
    
    def __init__(self, chat_model: ChatModel):
        """
        Initializes the ChatController with the provided ChatModel instance.

        Args:
        ----
        chat_model : ChatModel
            An instance of the ChatModel used to perform database operations.
        """
        self.chat_model = chat_model

    async def create_chat(self, chat: CreateChat, user_id: str) -> ChatInDB:
        """
        Creates a new chat and stores it in the database with a unique session ID.

        The method generates a new session ID and adds it to the chat before saving it
        to the database.

        Args:
        ----
        chat : CreateChat
            The data required to create a new chat.

        user_id: str
            The username for the user who wants to create the chat.    

        Returns:
        -------
        ChatInDB
            The newly created chat with the session ID and other database fields.
        """
        session_id = generate_session_id()  # Generate a unique session ID
        chat_dict = chat.dict()  # Convert CreateChat schema to dictionary
        chat_dict.update({"session_id": session_id, "user_id": user_id})  # Add session ID to the dictionary

        return await self.chat_model.create_chat(ChatInDB(**chat_dict))

    async def get_chat(self, session_id: str) -> ChatInDB:
        """
        Retrieves a specific chat from the database using the session ID.

        Args:
        ----
        session_id : str
            The unique identifier of the chat to retrieve.

        Returns:
        -------
        ChatInDB
            The chat object that corresponds to the given session ID, if it exists.
        """
        return await self.chat_model.get_chat(session_id)
    
    async def get_all_chats(self, user_id: str, limit: int = ChatSettings.CHATS_COUNT_LIMIT.value) -> list[ChatInDB]:
        """
        Retrieves all chats for a given user, limited to a certain number of chats.

        Args:
        ----
        user_id : str
            The unique identifier of the user whose chats are to be retrieved.
        limit : int, optional
            The maximum number of chats to retrieve. Defaults to the value in `ChatSettings.CHATS_COUNT_LIMIT`.

        Returns:
        -------
        list[ChatInDB]
            A list of all chats associated with the given user ID, limited by the `limit` argument.
        """
        return await self.chat_model.get_all_chats(user_id, limit)
    
    async def chat_exists(self, session_id: str, user_id: str) -> bool:
        """
        Checks if a chat with a specific session ID exists for a given user.

        Args:
        ----
        session_id : str
            The session ID of the chat to check.
        user_id : str
            The user ID to check if the chat exists for.

        Returns:
        -------
        bool
            True if the chat exists for the given session ID and user ID, False otherwise.
        """
        return await self.chat_model.chat_exists(session_id, user_id)
