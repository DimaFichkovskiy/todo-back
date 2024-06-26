from pymongo.collection import Collection
from passlib.context import CryptContext
from fastapi import HTTPException

from src import schemas, models, security

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCRUD:

    @classmethod
    async def get_user_by_email(cls, db: Collection, email: str) -> models.User:
        user = db.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
            return models.User(**user)
        else:
            return None

    @classmethod
    async def get_user_by_email_and_password(cls, db: Collection, email: str, password: str):
        user_data: models.User = await UserCRUD.get_user_by_email(db, email)
        if user_data:
            return await security.verify_password(
                password=password, hashed_password=user_data.hashed_password
            )
        else:
            return False

    @classmethod
    async def create_user(cls, db: Collection, sign_up_data: schemas.SignUp):
        hashed_password = await security.get_password_hash(password=sign_up_data.password)
        user = models.User(
            first_name=sign_up_data.first_name,
            last_name=sign_up_data.last_name,
            email=sign_up_data.email,
            hashed_password=hashed_password
        )
        response = db.insert_one(user.dict())

        return {"id": str(response.inserted_id), "email": user.email}
