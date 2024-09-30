from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION:str

    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = "/mnt/d/The-boy-who-lived/src/.env" # path problem


def get_settings():
    return Settings()