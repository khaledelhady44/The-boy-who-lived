from base_data_model import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.db.user import UserInDB
from ..enums import DataBaseEnum
from typing import Optional


class UserModel(BaseDataModel):

    """
    A class to manage user-related operations in the database.

    Attributes:
        collection (Collection): The MongoDB collection for user data.
    """ 

    def __init__(self, db_client: AsyncIOMotorClient): # type: ignore
        """
        Initializes the UserModel with the specified database client.

        Args:
            db_client (AsyncIOMotorClient): The asynchronous MongoDB client instance.
        """

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.USER_COLLECTION.value]

    async def create_user(self, user: UserInDB) -> None:
        """
        Inserts a new user into the database.

        Args:
            user (UserInDB): The user data to insert, represented as a UserInDB instance.

        Returns:
            None: This function does not return a value.
        """

        user_dict = user.dict()
        await self.collection.insert_one(user_dict)

    async def get_user(self, username: str) -> Optional[UserInDB]:
        """
        Retrieves a user from the database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[UserInDB]: The user data if found, otherwise None.
        """

        user_data = await self.collection.find_one({"username": username})
        if user_data:
            return UserInDB(**user_data)
        
        return None
        
    async def user_exists(self, username: str) -> bool:
        """
        Checks if a user with the given username exists in the database.

        Args:
            username (str): The username to check for existence.

        Returns:
            bool: True if the user exists, False otherwise.
        """

        user_data = await self.collection.find_one({"username": username})
        return user_data is not None