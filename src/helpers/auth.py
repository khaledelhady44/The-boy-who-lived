from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from helpers import Settings, get_settings
from fastapi import HTTPException, status
from pydantic import ValidationError


settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the stored hashed password.

    Parameters:
    ----------
    plain_password : str
        The plain text password provided by the user during login.
    
    hashed_password : str
        The hashed password stored in the database.

    Returns:
    -------
    bool
        True if the password matches the hashed password, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password to a secure, hashed version for storage.

    Parameters:
    ----------
    password : str
        The plain text password that needs to be hashed.

    Returns:
    -------
    str
        A hashed representation of the input password.
    """

    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token with an optional expiration time.

    Parameters:
    ----------
    data : dict
        The data to encode in the JWT, typically containing the user information.
    
    expires_delta : Optional[timedelta]
        Optional expiration time for the token. If not provided, the token will 
        expire in 30 minutes by default.

    Returns:
    -------
    str
        The encoded JWT access token.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> str:
    """
    Decodes a JWT access token to extract the user information (usually the username).

    Parameters:
    ----------
    token : str
        The JWT access token that needs to be decoded.
    
    Returns:
    -------
    str
        The username extracted from the token, if the token is valid.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

    except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return username