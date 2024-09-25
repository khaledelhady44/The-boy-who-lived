from fastapi import APIRouter, status, Request
from schemas.user import RegisterUser, UserInDB
from controllers.user_controller import UserController


register = APIRouter()


@register.post("/register", response_model=RegisterUser, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user: RegisterUser):
    """
    Register a new user in the application.

    This endpoint handles the registration of a new user by accepting 
    user data in the request body, creating a corresponding UserInDB object, 
    and delegating the registration logic to the UserController.

    Args:
        request (Request): The incoming HTTP request object, containing app-level 
                           dependencies like the user controller.
        user (RegisterUser): The user data provided in the request body. This is validated 
                     against the RegisterUser schema.

    Returns:
        RegisterUser: The registered user information.
    """

    user_controller = request.app.user_controller

    await user_controller.register(user=user)

    return user

    

