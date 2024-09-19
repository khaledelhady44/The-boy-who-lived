from helpers.config import get_settings, Settings

class BaseDataModel:
    """
    BaseDataModel is the foundational class for all data models in the application
    responsible for interacting with the database.

    Attributes:
    db_client: object:
        The database client instance.

    app_settings: Settings:
        Application-specific settings used for configuring various aspects of the
        application.
    """
    
    def __init__(self, db_client: object):
        self.db_client : object = db_client
        self.app_settings : Settings = get_settings