from fastapi import APIRouter, Request, HTTPException
from fastapi.security import HTTPBearer

from src import schemas
from src import models
from src.crud import UserCRUD
from src.routes.dependencies import get_current_user

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from src import security, utils

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not Found"}}
)


@router.post("/sign-in", status_code=200)
async def sign_in(request: Request, sing_in_data: schemas.SignIn = Depends()):
    db = request.app.users
    user = await UserCRUD.get_user_by_email(db=db, email=sing_in_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not await security.verify_password(sing_in_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": await utils.create_access_token(user.email),
        "refresh_token": await utils.create_refresh_token(user.email)
    }


@router.post("/sign-up", status_code=201)
async def sign_up(request: Request, sign_up_data: schemas.SignUp):
    db = request.app.users
    user_exist = await UserCRUD.get_user_by_email(db, sign_up_data.email)
    if user_exist:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    inserted_user = await UserCRUD.create_user(db, sign_up_data)
    return {
        "access_token": await utils.create_access_token(inserted_user["email"]),
        "refresh_token": await utils.create_refresh_token(inserted_user["email"])
    }


@router.get("/about-me", status_code=200)
async def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
