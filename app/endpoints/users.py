from fastapi import APIRouter
from fastapi import (
    APIRouter, 
    Body, 
    Depends, 
    Form, 
    HTTPException,
    status
)
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.user_schema import (
    User,
    UserPermission,
    Address
)
from app.db.permission_schema import (
    Permission,
    Council,
)
from app.db.session import get_db
from app.schema.user import (
    PermissionListSchema,
    PermissionSchema
)
from app.db.accessor import UserAccessor
from app.core.security import get_password_hash
from app.schema.user import UserBase
from app.endpoints.dependencies import get_current_user, get_current_active_user


router = APIRouter()

@router.post('/user')
async def insert_user(
    username: str = Form(),
    f_name: str = Form(),
    s_name: str = Form(),
    l_name: str = Form(),
    password: str = Form(),
    db_session: AsyncSession = Depends(get_db)
):
    user = User(
        username=username,
        f_name=f_name,
        s_name=s_name,
        l_name=l_name,
        password=get_password_hash(password=password)
    )
    await user.save(db_session)
    return user

@router.post('/council')
async def insert_council(
    value: str = Form(),
    db_session: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    print('hello', current_user.token)
    council = Council(
        value=value
    )
    await council.save(db_session)
    return council

@router.post('/permission')
async def insert_permission(
    name: str = Form(),
    db_session: AsyncSession = Depends(get_db)
):
    permission = Permission(
        name=name
    )
    await permission.save(db_session)
    return permission


@router.post('/user_permission')
async def insert_user_permission(
    user_id: int = Form(),
    permission_id: int = Form(),
    council_id: int = Form(),
    db_session: AsyncSession = Depends(get_db)
):
    data = UserPermission(
        user_id=user_id,
        permission_id=permission_id,
        council_id=council_id
    )
    await data.save(db_session)
    return data

@router.get('/show_permissions/{user_id}', response_model=PermissionListSchema)
async def get_permissions(
    user_id: int,
    db_session: AsyncSession = Depends(get_db)
):
    # ans = await UserPermission.get_council(
    #     db_session=db_session,
    #     user_id=id
    # )
    # resp = PermissionListSchema()
    # buf = []
    # for tpl in ans:
    #     x = tpl._asdict()
    #     buf.append(
    #         PermissionSchema(
    #             user_id=x['id'],
    #             permission_name=x['name'],
    #             council_name=x['value']
    #         )
    #     )
    # resp.list_permissions = buf
    
    # return resp
    
    ans = await UserAccessor.get_permissions(db_session=db_session, user_id=user_id)
    return ans

@router.post('/add_address')
async def add_address(
    user_id: int = Form(),
    email: str = Form(),
    db_session: AsyncSession = Depends(get_db)
):
    adress = Address(user_id=user_id, email_address=email)
    await adress.save(db_session=db_session)
    return status.HTTP_201_CREATED

@router.get('/get_addresses/{user_id}')
async def get_addresses(
    user_id: int,
    db_session: AsyncSession = Depends(get_db)
):
    await User.get_user_adresses(user_id=user_id, db_session=db_session)