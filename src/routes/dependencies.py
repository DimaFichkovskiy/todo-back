from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from src.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from src.crud import UserCRUD
from pymongo.collection import Collection
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

token_auth_scheme = HTTPBearer()

class TokenData(BaseModel):
    email: Optional[str] = None


async def get_user_by_email(db, email: str):
    user = await UserCRUD.get_user_by_email(db=db, email=email)
    return user


async def get_current_user(request: Request, token: str = Depends(token_auth_scheme)):
    db: Collection = request.app.users

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_str = token.credentials
        payload = jwt.decode(token_str, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
