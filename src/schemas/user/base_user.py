from pydantic import BaseModel, Field, EmailStr

class BaseUser(BaseModel):

    """
    BaseUser is a Pydantic model that represents the basic user information.

    Attributes:
    ----------
    username : str
        The unique username for the user. 
    
    email : EmailStr
        The user's email address.
    """

    username: str = Field(..., min_length=1)
    email: EmailStr
    

