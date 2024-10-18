from fastapi import APIRouter, status, Request
from schemas import LoginUser, Token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

login = APIRouter()

@login.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(request: Request, user_login: LoginUser) -> Token:
    """
    Handle user login by authenticating the provided username or email and password.

    - Returns a JSON object with the following fields:
        - `access_token`: The generated access token for the session.
        - `token_type`: The type of token, typically "bearer".
        - `username`: The username of the authenticated user.
        - `email`: The email of the authenticated user.
        - `full_name`: The full name of the authenticated user.

    Raises:
        - `HTTPException 400`: If neither username nor email is provided, a Bad Request is raised.
    """
    user_controller = request.app.user_controller
    access_token = await user_controller.authenticate_user(user_login)
    current_user = await user_controller.get_current_user(access_token.access_token)

    response = {
        "access_token": access_token.access_token,
        "token_type": access_token.token_type,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name
    }

    return response
