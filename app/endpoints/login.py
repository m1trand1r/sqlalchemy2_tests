from app.core.security import(
    get_password_hash,
    create_access_token
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter, 
    Body, 
    Depends, 
    Form, 
    HTTPException,
    status,
    Response
)

from app.endpoints.dependencies import (
    get_current_active_user,
    get_current_user
)
from app.schema.user import UserBase
from app.schema.token import Token, TokenPayload
from app.db.session import get_db
from app.db.accessor import UserAccessor
from app.core.security import vertify_password, get_password_hash


router = APIRouter()

async def authenticate_user(
    username: str,
    password: str,
    db_session: AsyncSession = Depends(get_db)
) -> UserBase:
    user = await UserAccessor.get_by_username(username=username, db_session=db_session)
    print(user)
    if not user:
        return False
    if not vertify_password(password, user.password):
        return False
    return True


@router.post('/login/token', response_model=Token)
async def token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db_session=db_session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect username or password'
        )
    