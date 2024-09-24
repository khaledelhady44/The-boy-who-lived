from pydantic import Field
from base_user import BaseUser

class RegisterUser(BaseUser):
    """
    RegisterUser is a Pydantic model that represents the user data required for registration.

    Attributes:
    ----------
    full_name : str
        The full name of the user.
    
    password : str
        The user's password.
    """

    full_name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)