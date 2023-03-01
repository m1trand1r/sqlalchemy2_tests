from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt_sha256

from app.core.config import settings

ALGORITHM = "HS512"

pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

def vertify_password(plain_pass: str, hashed_pass: str):
    return bcrypt_sha256.verify(plain_pass, hashed_pass)

def get_password_hash(password: str):
    return bcrypt_sha256.using(rounds=13, salt_size=22).hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt