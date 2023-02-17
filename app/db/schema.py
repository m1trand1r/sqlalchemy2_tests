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
    mapped_column
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # indexes
    'ix': 'ix__%(tablename)s__%(all_column_names)s',

    # unique indexes
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # CHECK-constrait ix
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # fk
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # pk
    'pk': 'pk__%(table_name)s'
}

custom_metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = custom_metadata
    
    async def save(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            return await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex)
            ) from ex
    
    async def delete(self, db_session: AsyncSession):
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex)
            ) from ex
            
    async def update(self, db_session: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        await self.save(db_session)
    

class User(Base):
    __tablename__ = 'user_account'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    f_name: Mapped[str] = mapped_column(String(20))
    s_name: Mapped[str] = mapped_column(String(20))
    l_name: Mapped[str] = mapped_column(String(20))
    addresses : Mapped[typing.List["Address"]] = relationship(back_populates='user', cascade='all, delete-orphan')
    
    
    
    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username}, fio={self.f_name + self.s_name + self.l_name})'
    
class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user_account.id"))
    email_address: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="addresses")
    
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
    
class Permission(Base):
    __tablename__ = 'permission'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
class Council(Base):
    __tablename__ = 'council'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(100))
    
    
class UserPermission(Base):
    __tablename__ = 'user_permission'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission.id"))
    council_id: Mapped[int] = mapped_column(ForeignKey("council.id"))
    
    @classmethod
    async def get_council(cls, db_session: AsyncSession, user_id: int):
        smth = (
            select(
                User.id,
                Permission.name,
                Council.value
            )
            .join(UserPermission, User.id == UserPermission.user_id)
            .join(Council)
            .join(Permission)
            .where(User.id == user_id)
        )
        res = await db_session.execute(smth)
        
        ans = res.all()
        print(ans)
        return ans
        
    
