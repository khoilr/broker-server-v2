import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from server.db.dao.user import UserDAO
from server.db.models.user import UserModel
from server.utils import auth
from server.web.api.user.schema import UserOutputDTO

router = APIRouter()


@router.post("/sign-in")
async def sign_in(input_data: OAuth2PasswordRequestForm = Depends()):
    # Generate token for user
    user = await auth.authenticate(input_data.username, input_data.password)
    token = auth.encode_token(data={"id": user.id})

    # Set header and content
    headers = {
        "Authorization": f"Bearer {token}",
    }
    content = json.dumps(
        {
            "access_token": token,
            "token_type": "bearer",
        },
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
    response_model=UserOutputDTO,
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


@router.get("/me", response_model=UserOutputDTO)
async def me(user: UserModel = Depends(auth.get_current_user)) -> UserModel:
    return user
