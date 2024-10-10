from helpers.config import get_settings
from fastapi import FastAPI
from routes import register, login, chat
from models.user_model import UserModel
from models.chat_model import ChatModel
from controllers.user_controller import UserController
from controllers.chat_controller import ChatController
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    app.user_model = UserModel(app.db_client)
    app.user_controller = UserController(app.user_model)

    app.chat_model = ChatModel(app.db_client)
    app.chat_controller = ChatController(app.chat_model)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(register)
app.include_router(login)
app.include_router(chat)