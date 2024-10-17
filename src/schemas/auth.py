from pydantic import BaseModel

class Token(BaseModel):
    """
    Token is a Pydantic model representing an access token for authentication.

    Attributes:
    ----------
    access_token : str
        The JWT access token that grants the user access to protected resources.
        
    token_type : str
        The type of token issued, typically set as "bearer" to indicate the authorization mechanism.
    """
    
    access_token: str
    token_type: str

    username: str | None = None
    email: str | None = None
    full_name: str | None = None



class TokenData(BaseModel):
    """
    TokenData is a Pydantic model representing the payload data contained within an access token.

    Attributes:
    ----------
    username : str | None
        The username associated with the token. This field is optional and may be None if not included in the token payload.
    """
    
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
