from fastapi import APIRouter, status
from ..schemas.requests.user import User
from ..schemas.db.user_in_db import UserInDB
from models.user_model import UserModel
from controllers.user_controller import UserController


register = APIRouter()
user_model = UserModel(db_client=)
user_controller = UserController(user_model)


@register.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    user_in_db = UserInDB(**user.dict())
    await user_controller.register(user=user_in_db)

    return user_in_db

    

