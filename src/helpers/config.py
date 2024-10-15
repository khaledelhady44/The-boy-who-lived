from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """
    Settings configuration class for loading environment variables.

    Attributes:
    ----------
    APP_NAME : str
        The name of the application.

    APP_VERSION : str
        The current version of the application.

    MONGODB_URL : str
        The connection URL for the MongoDB database.

    MONGODB_DATABASE : str
        The name of the MongoDB database.

    SECRET_KEY : str
        The secret key used for signing tokens.

    ALGORITHM : str
        The algorithm used for token signing.
    """
    
    APP_NAME: str
    APP_VERSION: str

    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"  # Relative path from the script's location


def get_settings() -> Settings:
    """
    Creates an instance of the Settings class and loads environment variables.

    Returns:
    -------
    Settings
        The settings instance containing the loaded environment variables.
    """
    return Settings()
