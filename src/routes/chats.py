from fastapi import APIRouter, status, Request, Depends, HTTPException
from schemas import ChatInDB, CreateChat, CreateMessage, MessageInDB
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

chat = APIRouter(prefix="/chats")

@chat.post("/", response_model=ChatInDB, status_code=status.HTTP_201_CREATED)
async def create_chat(request: Request, chat: CreateChat, token: str = Depends(oauth2_scheme)):
    """
    Creates a new chat for the current authenticated user.

    This endpoint allows a user to create a new chat by providing the necessary chat information.
    The current user's information is automatically extracted from the provided OAuth2 token.

    Args:
    ----
    request : Request
        The request object, used to access the application dependencies.
    token : str
        The OAuth2 token passed in the request for user authentication.

    Returns:
    -------
    ChatInDB
        The newly created chat object, including its unique session ID and user ID.
    """
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    current_user = await user_controller.get_current_user(token)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    return await chat_controller.create_chat(chat, current_user.username)

@chat.get("/", response_model=list[ChatInDB], status_code=status.HTTP_200_OK)
async def get_chats(request: Request, token: str = Depends(oauth2_scheme)):
    """
    Retrieves all chats for the current authenticated user.

    This endpoint retrieves a list of all chats that the current user is associated with.
    The number of chats returned is limited by the application settings.

    Args:
    ----
    request : Request
        The request object, used to access the application dependencies.
    token : str
        The OAuth2 token passed in the request for user authentication.

    Returns:
    -------
    list[ChatInDB]
        A list of chat objects associated with the current user.
    """
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    current_user = await user_controller.get_current_user(token)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return await chat_controller.get_all_chats(current_user.username)

@chat.post("/messages", status_code=status.HTTP_201_CREATED)
async def add_message(request: Request, message: CreateMessage, token: str = Depends(oauth2_scheme)):
    """
    Adds a new message to a specific chat for the current authenticated user.

    This endpoint allows a user to send a message in an existing chat. It checks if the user 
    is part of the chat and ensures the chat exists before allowing the message to be sent.

    Args:
    ----
    request : Request
        The request object, used to access the application dependencies.
    message : CreateMessage
        The message object that contains the content of the message.
    token : str
        The OAuth2 token passed in the request for user authentication.

    Returns:
    -------
    CreateMessage
        The message object that was added to the chat.
    
    Raises:
    ------
    HTTPException
        If the chat does not exist or if the user is not part of the chat.
    """
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    message_controller = request.app.message_controller

    current_user = await user_controller.get_current_user(token)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    # Check if the chat exists and if the user is part of it
    if not await chat_controller.chat_exists(message.chat_id, current_user.username):
        raise HTTPException(status_code=404, detail=f"Chat with id {message.chat_id} not found")
    
    # Create the message in the database
    await message_controller.create_message(message)
    
    return message

@chat.get("/{chat_id}/messages", response_model=list[MessageInDB], status_code=status.HTTP_200_OK)
async def get_messages(request: Request, chat_id: str, token: str = Depends(oauth2_scheme)):
    """
    Retrieves all messages for a specific chat for the current authenticated user.

    This endpoint fetches all the messages in a chat, ensuring that the user is part of the chat.

    Args:
    ----
    request : Request
        The request object, used to access the application dependencies.
    chat_id : str
        The unique identifier of the chat for which to retrieve messages.
    token : str
        The OAuth2 token passed in the request for user authentication.

    Returns:
    -------
    list[MessageInDB]
        A list of all messages in the specified chat, including their timestamp and content.
    
    Raises:
    ------
    HTTPException
        If the chat does not exist or if the user is not part of the chat.
    """
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    message_controller = request.app.message_controller

    current_user = await user_controller.get_current_user(token)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    # Check if the chat exists and if the user is part of it
    if not await chat_controller.chat_exists(chat_id, current_user.username):
        raise HTTPException(status_code=404, detail=f"Chat with id {chat_id} not found")
    
    # Fetch all messages in the chat
    return await message_controller.get_full_chat(chat_id)
