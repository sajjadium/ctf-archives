from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field

from mvmcryption.auth import (
    SJWT_TTL,
    AuthorizedUser,
    create_sjwt,
    decode_sjwt,
    global_sjwt,
)
from mvmcryption.crypto.jwt import SJWT
from mvmcryption.db.users import Users
from mvmcryption.environ import IS_DEV

USERNAME_FIELD = Field(max_length=50, min_length=2)
PASSWORD_FIELD = Field(max_length=100, min_length=8)


class LoginBody(BaseModel):
    username: str = USERNAME_FIELD
    password: str = PASSWORD_FIELD


class RegisterBody(BaseModel):
    email: EmailStr
    username: str = USERNAME_FIELD
    password: str = PASSWORD_FIELD


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/status")
def user_status(
    users: Annotated[Users, Depends(Users.dependency)],
    sjwt: Annotated[SJWT, Depends(global_sjwt)],
    mvmcryptionauthtoken: Annotated[str | None, Cookie()] = None,
):
    """Return whether or not user is logged in."""
    return {"authorized": bool(decode_sjwt(mvmcryptionauthtoken, sjwt, users))}


@auth_router.post("/login")
def login(
    body: LoginBody,
    response: Response,
    sjwt: Annotated[SJWT, Depends(global_sjwt)],
    users: Annotated[Users, Depends(Users.dependency)],
):
    if not (user := users.login(body.username, body.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials.",
        )
    expires = datetime.now(UTC) + SJWT_TTL
    token = create_sjwt(user, sjwt, expires)
    response.set_cookie(
        "mvmcryptionauthtoken",
        token,
        expires=expires,
        secure=not IS_DEV,
        httponly=True,
    )
    response.status_code = status.HTTP_204_NO_CONTENT


@auth_router.post("/register")
def register(
    body: RegisterBody,
    users: Annotated[Users, Depends(Users.dependency)],
):
    if users.find_by_username(body.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is not available.",
        )
    email = body.email.lower()
    if users.find_by_username(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not available.",
        )
    if not (
        user := users.create(
            username=body.username,
            email=email,
            password=body.password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Something went very wrong.",
        )
    return user


@auth_router.post("/logout")
def logout(response: Response, user: AuthorizedUser):
    response.delete_cookie("mvmcryptionauthtoken")
    response.status_code = status.HTTP_204_NO_CONTENT
