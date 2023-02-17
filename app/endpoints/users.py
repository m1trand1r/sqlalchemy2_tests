from fastapi import APIRouter
from fastapi import (
    APIRouter, 
    Body, 
    Depends, 
    Form, 
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schema import (
    User,
    Permission,
    Council,
    UserPermission,
    Address
)
from app.db.session import get_db


router = APIRouter()

@router.post('/user')
async def insert_user(
    username: str = Form(),
    f_name: str = Form(),
    s_name: str = Form(),
    l_name: str = Form(),
    db_session: AsyncSession = Depends(get_db)
):
    user = User(
        username=username,
        f_name=f_name,
        s_name=s_name,
        l_name=l_name
    )
    await user.save(db_session)
    return user