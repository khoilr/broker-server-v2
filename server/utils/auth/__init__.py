from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from server.utils.auth.password import verify_password
from server.db.dao.user import UserDAO
from server.db.models.user import UserModel

SECRET_KEY = "8fdd23c03a106a4767f889e52d64f86671c0ffdd911f82ff1d0a6f686838ce77"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def authenticate(username: str, password: str) -> UserModel:
    user_dao = UserDAO()
    user = await user_dao.get(username=username)

    return user if verify_password(password, user.password) else None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    user_dao = UserDAO()
    user = decode_token(token)
    return await user_dao.get(id=user["id"])


async def is_user_exist(username: str) -> bool:
    user_dao = UserDAO()
    user = await user_dao.get(username=username)
    return user is not None


def encode_token(data: dict) -> str:
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
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
