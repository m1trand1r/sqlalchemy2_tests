from sqlalchemy import (
    MetaData,
    ForeignKey,
    func,
    Integer,
    String
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
