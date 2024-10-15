from enum import Enum

class Auth(Enum):
    """
    Enum class that defines authentication-related settings for the application.

    Attributes:
    ----------
    ACCESS_TOKEN_EXPIRE_MINUTES : int
        The number of minutes after which the access token expires.
    """
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 300  # Token expires in 300 minutes (5 hours)
