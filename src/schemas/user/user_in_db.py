from pydantic import Field
from schemas.user import BaseUser
from bson.objectid import ObjectId

class UserInDB(BaseUser):
    """
    UserInDB is a Pydantic model that represents the user data stored in the database.
    
    Attributes:
    ----------
    full_name : str
        The full name of the user.
    
    hashed_password : str
        The hashed password of the user. This field is required to store the user's password securely.

    id : str
        The unique identifier for the user in the database. It defaults to a newly generated ObjectId, ensuring uniqueness.

    """
    
    full_name: str = Field(..., min_length=1)
    hashed_password: str = Field(..., min_lenght = 1)
    id: str = Field(default_factory=lambda: str(ObjectId()))