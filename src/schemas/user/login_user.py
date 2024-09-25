from schemas.user  import BaseUser
from pydantic import Field, EmailStr

class LoginUser(BaseUser):
    """
    LoginUser is a Pydantic model that represents the user data required for login.

    Attributes:
    ----------
    username : str | None
        The username used for login. It is an optional field that may be left empty.

    email : EmailStr | None
        The email address used for login. It is an optional field that may be left empty. 

    password : str
        The user's password, required for login.
    """

    email: EmailStr | None = None
    password: str = Field(..., min_length = 1)