from fastapi import APIRouter, status, Request, Depends, HTTPException
from schemas.chat import ChatInDB, CreateChat
from schemas.message import CreateMessage, MessageInDB
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

@chat.post("/{chat_id}/messages", status_code = status.HTTP_201_CREATED)
async def add_message(request: Request, message: CreateMessage, token: str = Depends(oauth2_scheme)):
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    message_controller = request.app.message_controller

    current_user = await user_controller.get_current_user(token)

    if(not chat_controller.chat_exists(message.chat_id, current_user.username)):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    
    await message_controller.create_message(message)    
    return message

@chat.get("/{chat_id}/messages", response_model = list[MessageInDB], status_code=status.HTTP_200_OK)
async def get_messages(request: Request, chat_id: str, token: str = Depends (oauth2_scheme)):
    chat_controller = request.app.chat_controller
    user_controller = request.app.user_controller
    message_controller = request.app.message_controller

    current_user = await user_controller.get_current_user(token)

    if(not chat_controller.chat_exists(chat_id, current_user.username)):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return await message_controller.get_full_chat(chat_id)
    

    