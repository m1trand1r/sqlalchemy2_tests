from __future__ import annotations

from sqlalchemy import (
    MetaData,
    ForeignKey,
    func,
    Integer,
    String,
    select
)
import typing

from fastapi import HTTPException, status
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped, 
    relationship,
    mapped_column,
    selectinload
)
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base


class User(Base):
    __tablename__ = 'user_account'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    f_name: Mapped[str] = mapped_column(String(20))
    s_name: Mapped[str] = mapped_column(String(20))
    l_name: Mapped[str] = mapped_column(String(20))
    addresses : Mapped[typing.List[Address]] = relationship(lazy='raise')
    
    
    
    # def __repr__(self) -> str:
    #     return f'User(id={self.id}, username={self.username}, fio={self.f_name + self.s_name + self.l_name})'
    # @staticmethod
    # async def get_user_adresses(user_id, db_session: AsyncSession):
    #     smth = select(User).options(selectinload(User.addresses)).where(User.id == user_id)
    #     res = await db_session.scalars(smth)
    #     for i in res:
    #         for j in i.addresses:
    #             print(j.email_address)

    
class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user_account.id"))
    email_address: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address})"
    
class UserPermission(Base):
    __tablename__ = 'user_permission'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission.id"))
    council_id: Mapped[int] = mapped_column(ForeignKey("council.id"))

    # @classmethod
    # async def get_council(cls, db_session: AsyncSession, user_id: int):
    #     smth = (
    #         select(
    #             User.id,
    #             Permission.name,
    #             Council.value
    #         )
    #         .join(UserPermission, User.id == UserPermission.user_id)
    #         .join(Council)
    #         .join(Permission)
    #         .where(User.id == user_id)
    #     )
    #     res = await db_session.execute(smth)
        
    #     ans = res.all()
    #     print(ans)
    #     return ans