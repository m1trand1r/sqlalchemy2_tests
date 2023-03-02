from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    user_fio: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None