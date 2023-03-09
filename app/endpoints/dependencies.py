from app.db.session import get_db
from app.core.cookie_token import OAuth2PasswordBearerWithCookie
from app.schema.user import UserBase
from app.core import security
from app.core.config import settings
from app.schema.token import (
    Token,
    TokenPayload
)
from app.db.accessor import UserAccessor


from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import re


oauth_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl='/login/token'
)

async def get_current_user(
    db_session: AsyncSession = Depends(get_db),
    token: str = Depends(oauth_scheme)
) -> UserBase:
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        # print(payload)
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Could not validate creditenals',
        )
    user = await UserAccessor.get_by_username(db_session, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    user.token = token_data
    return user
    # return UserBase(**convert_to_dict(user))
    # TODO Дописать

async def get_current_active_user(current_user: UserBase = Depends(get_current_user)) -> UserBase:
    if not current_user.token.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )
    return current_user
