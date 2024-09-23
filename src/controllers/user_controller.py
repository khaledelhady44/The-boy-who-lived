from models import UserModel
from schemas.db import UserInDB
from fastapi import HTTPException, status

class UserController:
    """
    UserController handles user-related operations, such as registration.

    Attributes:
        user_model (UserModel): An instance of UserModel used for database operations.
    """

    def __init__(self, user_model: UserModel):
        """
        Initializes the UserController with a specified UserModel.

        Args:
            user_model (UserModel): An instance of UserModel that provides 
            methods for interacting with the user database.
        """

        self.user_model = user_model

    async def register(self, user: UserInDB) -> bool:
        """
        Registers a new user in the system.

        This method checks if the user already exists. If the username 
        is already taken, an HTTPException is raised. If the user does 
        not exist, the user is created in the database.

        Args:
            user (UserInDB): An instance of UserInDB containing user 
            information required for registration.

        Raises:
            HTTPException: If the username already exists, a 400 status code 
            is returned with a relevant error message.

        Returns:
            bool: Returns True if the user registration is successful.
        """
        
        if await self.user_model.user_exists(user):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Username already in use")
        
        await self.user_model.create_user(user)
        return True
