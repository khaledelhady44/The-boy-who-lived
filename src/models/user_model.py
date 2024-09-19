from base_data_model import BaseDataModel
from .db_schemas import user
from .enums import DataBaseEnum


class UserModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.USER_COLLECTION.value]

    