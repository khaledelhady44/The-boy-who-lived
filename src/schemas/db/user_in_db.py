from pydantic import Field
from ..requests import User
from bson.objectid import ObjectId

class UserInDB(User):
    """
    A Pydantic model representing a user stored in the database.

    Inherits all attributes from the User model and adds a unique identifier.

    Attributes:
        id (str): A unique identifier for the user, generated using ObjectId from MongoDB.
    """
    
    id: str = Field(default_factory=lambda: str(ObjectId()))