from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Bundle
from fastapi import status

from app.db.permission_schema import (
    Permission,
    Council
)
from app.db.user_schema import (
    User,
    UserPermission,
    Address
)
from app.schema.user import PermissionListSchema, PermissionSchema, UserBase


class UserAccessor:
    @staticmethod
    async def get_by_username(db_session: AsyncSession, username: int) -> UserBase | None:
        prep = await db_session.execute(
            select(User)
            .where(User.username == username)
        )
        res = prep.first()
        if res:
            return UserBase(**res)
        else:
            raise status.HTTP_404_NOT_FOUND
    
    @staticmethod
    async def get_permissions(db_session: AsyncSession, user_id: int):
        # bndl = Bundle('user_permissions', User.id, Permission.name, Council.value)
        smth = (
            select(
                User.id,
                Permission.name,
                Council.value
                # bndl
            )
            .join(UserPermission, User.id == UserPermission.user_id)
            .join(Council)
            .join(Permission)
            .where(User.id == user_id)
        )
        prep = await db_session.execute(smth)
        res = prep.all()
        buf = []
        for tpl in res:
            buf.append(
                PermissionSchema(**tpl._asdict())
            )
        return PermissionListSchema(list_permissions=buf)
    