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
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base

class Permission(Base):
    __tablename__ = 'permission'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
class Council(Base):
    __tablename__ = 'council'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(100))