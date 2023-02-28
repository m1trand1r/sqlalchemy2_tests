from pydantic import BaseModel
from typing import List

class PermissionSchema(BaseModel):
    user_id: int
    permission_name: str
    council_name: str
    
    
class PermissionListSchema(BaseModel):
    list_permissions: List[PermissionSchema] | None