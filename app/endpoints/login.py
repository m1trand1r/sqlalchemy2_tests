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
    Response,
    
)
from datetime import timedelta
from app.endpoints.dependencies import (
    get_current_active_user,
    get_current_user
)
from starlette.responses import RedirectResponse
from app.core.config import settings
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
    if not vertify_password(password, user.hashed_password):
        return False
    return user


@router.post('/login/token')
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
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key='access_token',
        value=f'Bearer {access_token}',
        httponly=True,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.get('/logout')
async def logout_remove_cookie(response: Response):
    response.delete_cookie(key='access_token')
    return status.HTTP_200_OK