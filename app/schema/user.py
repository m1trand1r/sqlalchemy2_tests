from pydantic import BaseModel
from typing import List

class PermissionSchema(BaseModel):
    id: int
    name: str
    value: str
    
    
class PermissionListSchema(BaseModel):
    list_permissions: List[PermissionSchema] | None