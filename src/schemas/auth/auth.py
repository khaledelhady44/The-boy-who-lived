from pydantic import BaseModel

class Token(BaseModel):
    """
    Represents an access token model for the authentication system.

    Attributes:
        access_token (str): The JWT access token that grants access to protected resources.
        token_type (str): The type of token issued, typically "bearer".
    """

    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Represents the data contained within the access token.

    Attributes:
        username (str | None): The username associated with the token. It can be None if not specified.
    """
    
    username: str | None = None