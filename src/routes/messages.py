import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas import CreateMessage, MessageInDB
from controllers import UserController, ChatController, MessageController
from helpers import get_user_controller, get_chat_controller, get_message_controller
from llm import get_harry_answer
import asyncio

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
message = APIRouter(prefix="/chats")


class ConnectionManager:
    """
    Manages WebSocket connections and message broadcasting for active chats.

    Attributes:
        active_connections (dict[str, list[WebSocket]]): A dictionary storing lists of active WebSocket connections
        for each chat ID.

    Methods:
        connect(websocket, chat_id): Adds a new WebSocket connection to a chat.
        disconnect(websocket, chat_id): Removes a WebSocket connection from a chat.
        send_message_to_chat(message, sender, chat_id): Broadcasts a message to all participants in a chat.
        send_history(history, chat_id): Sends the chat history to all participants in a chat.
    """

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        """
        Accepts a WebSocket connection and adds it to the specified chat.

        Args:
            websocket (WebSocket): The WebSocket connection to manage.
            chat_id (str): The ID of the chat to connect to.
        """
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: str):
        """
        Removes a WebSocket connection from the specified chat.

        Args:
            websocket (WebSocket): The WebSocket connection to remove.
            chat_id (str): The ID of the chat to disconnect from.
        """
        self.active_connections[chat_id].remove(websocket)
        if len(self.active_connections[chat_id]) == 0:
            del self.active_connections[chat_id]

    async def send_message_to_chat(self, message: str, sender: str, chat_id: str):
        """
        Sends a message to all participants in a specific chat.

        Args:
            message (str): The content of the message to send.
            sender (str): The sender of the message ("USER" or "SYSTEM").
            chat_id (str): The ID of the chat to send the message to.
        """
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                response = {"sender": sender, "message": message}
                await connection.send_json(json.dumps(response))

    async def send_history(self, history: list[MessageInDB], chat_id: str):
        """
        Sends the chat history to all participants in a chat.

        Args:
            history (list[MessageInDB]): A list of messages from the chat history.
            chat_id (str): The ID of the chat.
        """
        for message in history:
            await self.send_message_to_chat(message.message, message.sender, chat_id)


manager = ConnectionManager()


async def verify(chat_id: str, user_controller: UserController, chat_controller: ChatController, token: str = None):
    """
    Verifies the validity of the user's token and checks if they are authorized to access the specified chat.

    Args:
        chat_id (str): The ID of the chat to verify access for.
        user_controller (UserController): The user controller for managing user operations.
        chat_controller (ChatController): The chat controller for managing chat operations.
        token (str, optional): The user's token for authentication. Defaults to None.

    Raises:
        WebSocketException: If the token is invalid or the user is unauthorized.
    """
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
async def send_message(
    websocket: WebSocket,
    chat_id: str,
    user_controller: UserController = Depends(get_user_controller),
    chat_controller: ChatController = Depends(get_chat_controller),
    message_controller: MessageController = Depends(get_message_controller),
):
    """
    WebSocket endpoint for managing real-time communication within a specific chat.

    Args:
        websocket (WebSocket): The WebSocket connection for the chat.
        chat_id (str): The ID of the chat.
        user_controller (UserController): The user controller dependency.
        chat_controller (ChatController): The chat controller dependency.
        message_controller (MessageController): The message controller dependency.

    Raises:
        Exception: If any error occurs during WebSocket communication.
    """
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
                chat_id=chat_id,
                sender="USER",
                message=data
            )

            await message_controller.create_message(user_message)
            await manager.send_message_to_chat(user_message.message, "USER", chat_id)

            await asyncio.sleep(0)

            output = get_harry_answer(data, chat_id)

            harry_message = CreateMessage(
                chat_id=chat_id,
                sender="SYSTEM",
                message=output
            )

            await message_controller.create_message(harry_message)
            await manager.send_message_to_chat(harry_message.message, "SYSTEM", chat_id)

            await asyncio.sleep(0)

    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
