import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas import CreateMessage, MessageInDB
from controllers import UserController, ChatController, MessageController
from helpers import get_user_controller, get_chat_controller, get_message_controller
from llm import app
from langchain.schema import  HumanMessage


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
message = APIRouter(prefix="/chats")

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()

        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: str):
        self.active_connections[chat_id].remove(websocket)
        if len(self.active_connections[chat_id]) == 0:
            del self.active_connections[chat_id]

    async def send_message_to_chat(self, message: str, sender: str, chat_id: str):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                response = {"sender": sender, "message": message}
                await connection.send_json(json.dumps(response))
    
    async def send_history(self, history: list[MessageInDB], chat_id):
        for message in history:
            await self.send_message_to_chat(message.message, message.sender, chat_id)

manager = ConnectionManager()

async def verify(chat_id: str, user_controller: UserController, chat_controller: ChatController, token: str= None):
    if token is None or not token.startswith("Bearer "):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or Expired token")

    token = token.split(" ")[1]
    try:
        current_user = await user_controller.get_current_user(token)
    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or Expired token")
    

    if not await chat_controller.chat_exists(chat_id, current_user.username):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="No such User or chat")

@message.websocket("/{chat_id}/send")
async def send_message(websocket: WebSocket, chat_id: str, user_controller: UserController = Depends(get_user_controller),
                                                            chat_controller: ChatController = Depends(get_chat_controller),
                                                            message_controller: MessageController = Depends(get_message_controller)):
    
    token = websocket.headers.get("Authorization")

    try:
        await verify(chat_id, user_controller, chat_controller, token)
    except Exception as e:
        raise e
        
    await manager.connect(websocket, chat_id)

    history = await message_controller.get_full_chat(chat_id)
    await manager.send_history(history, chat_id)

    try:
        while True:
            data = await websocket.receive_text()

            user_message = CreateMessage(
                chat_id =  chat_id,
                sender = "USER",
                message = data
            )

            config = {"configurable": {"thread_id": chat_id}}
            input_messages = [HumanMessage(data)]
            output = app.invoke({"messages": input_messages}, config)

            harry_message = CreateMessage(
                chat_id = chat_id,
                sender = "SYSTEM",
                message = output["messages"][-1].content
            )

            await message_controller.create_message(user_message)
            await message_controller.create_message(harry_message)

            await manager.send_message_to_chat(user_message.message,"USER", chat_id)
            await manager.send_message_to_chat(harry_message.message,"SYSTEM", chat_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
        
        
    
    
            