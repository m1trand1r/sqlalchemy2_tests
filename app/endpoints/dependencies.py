from app.db.session import get_db
from app.core.cookie_token import OAuth2PasswordBearerWithCookie
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import re


oauth_scheme = OAuth2PasswordBearer(
    tokenUrl='/token'
)

async def get_current_user(
    db_session: AsyncSession = Depends(get_db),
    token: str = Depends(oauth_scheme)
) -> UserBase:
    try:
        # print(token)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        # print(payload)
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate creditenals',
        )
    user = CRUDUser.get_by_email(db, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return UserBase(**convert_to_dict(user))