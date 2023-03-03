from pydantic import BaseModel
from typing import List
from app.schema.token import TokenPayload

class PermissionSchema(BaseModel):
    id: int
    name: str
    value: str
    
    
class PermissionListSchema(BaseModel):
    list_permissions: List[PermissionSchema] | None
    
class UserBase(BaseModel):
    username: str
    f_name: str # Имя
    s_name: str # Фамилия
    token: TokenPayload | None
    l_name: str # Отчество
    hashed_password: str
    