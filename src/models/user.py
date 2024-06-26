from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: Optional[str] = Field(default_factory=str, alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    date_registration: datetime = Field(default_factory=datetime.now)
