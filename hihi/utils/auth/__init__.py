from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from hihi.db.dao.user_dao import UserDAO
from hihi.db.models.user_model import UserModel

SECRET_KEY = "8fdd23c03a106a4767f889e52d64f86671c0ffdd911f82ff1d0a6f686838ce77"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign-in")


async def get_user(username: str):
    return await UserDAO.get(None, username)


async def get_current_active_user(current_user: Annotated[UserModel, Depends(get_user)]):
    return UserDAO.get(None, current_user.username)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate(username: str, password: str) -> bool:
    user = await UserDAO.get(None, username)
    return False if user is None else verify_password(password, user.password)


async def is_user_exist(username: str) -> bool:
    user = await get_user(username)
    return user is not None


def create_access_token(data: dict):
    # Create a copy of data to avoid changing the original data
    to_encode = data.copy()

    # Set expire time
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})

    # Encode data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return encoded data
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
