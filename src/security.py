from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from src.config import Config


import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# async def create_access_token(email: str, expires_delta: timedelta = None) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode = {"exp": expire, "email": email}
#     encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ENCODE_ALGORITHM)
#     return encoded_jwt

async def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
