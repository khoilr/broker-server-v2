"""
Initialize authentication.

Raises:
    HTTPException: HTTPException error code

Returns:
    None: None
"""

import os
from datetime import datetime, timedelta
from typing import Any, Union

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from server.db.dao.user import UserDAO
from server.db.models.user import UserModel
from server.utils.auth.password import verify_password

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def authenticate(username: str, password: str) -> Union[UserModel, None]:
    """
    Authenticate user.

    Args:
        username (str): Username
        password (str): Password

    Returns:
        Union[UserModel, None]: User object or None
    """
    user_dao = UserDAO()
    user = await user_dao.get(username=username)
    if user is not None:
        return user if verify_password(password, user.password) else None
    return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> Union[UserModel, None]:
    """
    Get current user from token.

    Args:
        token (str): token. Defaults to Depends(oauth2_scheme).

    Returns:
        Union[UserModel, None]: User object or None
    """
    user_dao = UserDAO()
    user = decode_token(token)
    return await user_dao.get(id=user["id"])


async def is_user_exist(username: str) -> bool:
    """
    Check if the user already exists.

    Args:
        username (str): username

    Returns:
        bool: User existing condition
    """
    user_dao = UserDAO()
    user = await user_dao.get(username=username)
    return user is not None


def encode_token(data: dict[str, Any]) -> str:
    """
    Encode token.

    Args:
        data (dict[str, Any]): data to encode

    Returns:
        str: encoded token
    """
    # Create a copy of data to avoid changing the original data
    to_encode = data.copy()

    # Set expire time
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})

    # Encode data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return encoded data
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode token from original one.

    Args:
        token (str): Token to decode

    Raises:
        HTTPException: HTTP Exception

    Returns:
        dict[str, Any]: decoded token or error
    """
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
