from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserModel, ChatModel, MessageModel
from controllers import UserController, ChatController, MessageController

settings = get_settings()
mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
db_client = mongo_conn[settings.MONGODB_DATABASE]


user_model = UserModel(db_client)
user_controller = UserController(user_model)

chat_model = ChatModel(db_client)
chat_controller = ChatController(chat_model)

message_model = MessageModel(db_client)
message_controller = MessageController(message_model)

def get_mongo_conn():
    return mongo_conn

def get_db():
    return db_client[settings.MONGODB_DATABASE]

def get_user_model():
    return user_model

def get_chat_model():
    return chat_model

def get_message_model():
    return message_model

def get_user_controller():
    return user_controller

def get_chat_controller():
    return chat_controller

def get_message_controller():
    return message_controller
    
