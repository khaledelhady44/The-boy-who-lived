from helpers import (get_db, get_user_controller, get_chat_controller, get_chat_model, get_message_controller, 
                     get_message_model, get_user_model, get_mongo_conn)
from fastapi import FastAPI
from routes import register, login, chat, message


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():

    app.mongo_conn = get_mongo_conn()
    app.db_client = get_db()

    app.user_model = get_user_model()
    app.user_controller = get_user_controller()

    app.chat_model = get_chat_model()
    app.chat_controller = get_chat_controller()

    app.message_model = get_message_model()
    app.message_controller = get_message_controller()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(register)
app.include_router(login)
app.include_router(chat)
app.include_router(message)