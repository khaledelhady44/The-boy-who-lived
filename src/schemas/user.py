from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId

class BaseUser(BaseModel):
    """
    BaseUser is a Pydantic model representing the basic information required for a user.

    Attributes:
    ----------
    username : str
        The unique username of the user. This field must contain at least one character.
    
    email : EmailStr
        The email address of the user, validated as a proper email format.
    """

    username: str = Field(..., min_length=1)
    email: EmailStr


class LoginUser(BaseUser):
    """
    LoginUser is a Pydantic model representing the required data for a user login.

    Attributes:
    ----------
    username : str | None
        The username used to log in. This field is optional and can be omitted during login.

    email : EmailStr | None
        The email address used to log in. This field is also optional and can be omitted.

    password : str
        The password for the user account. This field is required and must contain at least one character.
    """

    email: EmailStr | None = None
    password: str = Field(..., min_length=1)


class RegisterUser(BaseUser):
    """
    RegisterUser is a Pydantic model representing the data required to register a new user.

    Attributes:
    ----------
    full_name : str
        The full name of the user. This field must contain at least one character.
    
    password : str
        The password for the user account. This field is required and must contain at least one character.
    """

    full_name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserInDB(BaseUser):
    """
    UserInDB is a Pydantic model representing the data stored in the database for a user.

    Attributes:
    ----------
    full_name : str
        The full name of the user. This field must contain at least one character.

    hashed_password : str
        The hashed version of the user's password. This field is required to store the password securely.

    id : str
        The unique identifier for the user in the database. Defaults to a newly generated ObjectId for uniqueness.
    """

    full_name: str = Field(..., min_length=1)
    hashed_password: str = Field(..., min_length=1)
    id: str = Field(default_factory=lambda: str(ObjectId()))
