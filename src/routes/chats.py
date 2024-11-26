from fastapi import APIRouter, status, Request, Depends, HTTPException
from schemas import ChatInDB, CreateChat, CreateMessage, MessageInDB
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

chat = APIRouter(prefix="/chats")

@chat.post("/create", response_model=ChatInDB, status_code=status.HTTP_201_CREATED)
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

    try:
        current_user = await user_controller.get_current_user(token)
    except Exception as e:
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

    try:
        current_user = await user_controller.get_current_user(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") 

    return await chat_controller.get_all_chats(current_user.username)