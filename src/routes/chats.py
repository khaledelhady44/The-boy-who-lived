from fastapi import APIRouter, status, Request, Depends
from schemas.chat import BaseChat, ChatInDB, CreateChat
from schemas.user import UserInDB
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

chat = APIRouter(prefix = "/chats")

@chat.post("/", response_model = ChatInDB, status_code = status.HTTP_201_CREATED)
async def create_chat(request: Request, token: str = Depends(oauth2_scheme)):
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    current_user = await user_controller.get_current_user(token)
    chat_dict = {}

    chat_dict.update({"user_id": current_user.username})
    return await chat_controller.create_chat(CreateChat(**chat_dict))

@chat.get("/", response_model = list[ChatInDB])
async def get_chats(request: Request, token: str = Depends(oauth2_scheme)):
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    current_user = await user_controller.get_current_user(token)


    return await chat_controller.get_all_chats(current_user.username)


    