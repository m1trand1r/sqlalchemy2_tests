from __future__ import annotations

from sqlalchemy import (
    MetaData,
)
import typing

from fastapi import HTTPException, status
from sqlalchemy.orm import (
    DeclarativeBase
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