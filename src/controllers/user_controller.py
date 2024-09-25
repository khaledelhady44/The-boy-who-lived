from models import UserModel
from schemas.user import UserInDB, RegisterUser, LoginUser
from fastapi import HTTPException, status
from helpers import verify_password, create_access_token
from datetime import timedelta
from helpers import get_password_hash

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

    async def register(self, user: RegisterUser) -> bool:
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

        user_dict = user.dict()
        user_dict.update({"hashed_password": get_password_hash(user_dict["password"])})
        user_in_db = UserInDB(**user_dict)
        
        if await self.user_model.username_exists(user_in_db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Username already in use")
        elif await self.user_model.email_exists(user_in_db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "email already in use")
        
        await self.user_model.create_user(user_in_db)
        return True
    
    async def authenticate_user(self, user: LoginUser) -> str:
        username = user.username
        password = user.password

        user: UserInDB = await self.user_model.get_user(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid credentials",
                headers = {"WWW-Authenticate": "Bearer"}
            )
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid Credentials",
                headers = {"WWW-Authenticate": "Bearer"}
            )
        
        access_token_expires = timedelta(minutes = 30)
        access_token = create_access_token(
            data = {"sub": user.username},
            expires_delta=access_token_expires
        )

        return access_token
        

