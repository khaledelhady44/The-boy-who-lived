from helpers.config import get_settings
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    app.db_client["coll"].insert_one({"key": "value"})

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()