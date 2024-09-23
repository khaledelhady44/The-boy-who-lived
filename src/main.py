from helpers.config import get_settings
from fastapi import FastAPI
from routes import register
from models.user_model import UserModel
from controllers.user_controller import UserController
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    app.user_model = UserModel(app.db_client)
    app.user_controller = UserController(app.user_model)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(register)