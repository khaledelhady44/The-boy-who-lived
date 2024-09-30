from fastapi import APIRouter, status, Request, Depends, HTTPException
from schemas.user import LoginUser
from fastapi.security import OAuth2PasswordBearer
from schemas.auth import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

login = APIRouter()

@login.post("/login", response_model=Token)
async def login_user(request: Request, user_login: LoginUser) -> Token:
    """
    Handle user login by authenticating the provided username or email and password.

    Parameters:
    - request (Request): The FastAPI request object, which contains the application state.
    - user_login (LoginUser): The login details containing either the username or email, and the password.

    Returns:
    - Token: Represents an access token model for the authentication system..

    Raises:
    - HTTPException: If neither username nor email is provided, a 400 Bad Request is raised.
    """

    user_controller = request.app.user_controller

    if not user_login.username and not user_login.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either username or email."
        )
    access_token = await user_controller.authenticate_user(user_login)

    return access_token

@login.get("/profile", response_model=TokenData)
async def read_users_me(request: Request, token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Retrieve the current authenticated user's profile.

    Parameters:
    - request (Request): The FastAPI request object, which contains the application state.
    - token (str): The JWT token provided for authorization, passed through the `Depends` function.

    Returns:
    - TokenData: Represents the data contained within the access token.
    """

    user_controller = request.app.user_controller
    current_user = await user_controller.get_current_user(token)
    return current_user