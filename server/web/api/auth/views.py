import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from server.db.dao.user_dao import UserDAO
from server.db.models.user_model import UserModel
from server.utils import auth
from server.web.api.user.schema import UserOutputModelDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


@router.post("/sign-in")
async def sign_in(input_data: OAuth2PasswordRequestForm = Depends()):
    # Set header for response
    headers = {
        "Authorization": f"Bearer {input_data.username}",
    }

    # Response content
    content = json.dumps(
        {
            "access_token": input_data.username,
            "token_type": "bearer",
        }
    )

    # Create response
    response = Response(
        content=content,
        headers=headers,
        status_code=201,
    )

    # Return response
    return response


@router.post(
    "/sign-up",
    response_model=UserOutputModelDTO,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_dao: UserDAO = Depends(),
) -> UserModel:
    # Destructuring
    username = form_data.username
    password = form_data.password

    # Raise error if user already exist
    if await auth.is_user_exist(username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Hash password
    hashed_password = auth.hash_password(password)

    # Create user
    return await user_dao.create(
        name=username,
        username=username,
        password=hashed_password,
    )
