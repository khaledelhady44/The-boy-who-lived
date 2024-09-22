from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    """
    A Pydantic model representing a user for database storage.

    Attributes:
        username (str): The user's username (must be at least 1 character long).
        email (EmailStr): The user's email address.
        password (str): The user's password (must be at least 1 character long).
        full_name (str): The user's full name (must be at least 1 character long).
    """

    username: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1)
    full_name: str = Field(..., min_length=1)
