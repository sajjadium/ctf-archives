from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr

from mvmcryption.auth import AuthorizedUser
from mvmcryption.db import Users
from mvmcryption.resp import PERMISSION_DENIED, not_found
from mvmcryption.routers.auth import USERNAME_FIELD

users_router = APIRouter(prefix="/users", tags=["users"])


class UpdateBody(BaseModel):
    username: str = USERNAME_FIELD
    email: EmailStr


@users_router.get("/")
def user_list(
    user: AuthorizedUser,
    users: Annotated[Users, Depends(Users.dependency)],
):
    if user.is_admin:
        return users.all()
    return [user]


@users_router.patch("/{user_id}")
def update_user(
    user: AuthorizedUser,
    users: Annotated[Users, Depends(Users.dependency)],
    user_id: int | Literal["me"],
    body: UpdateBody,
):
    """Whoa! im updating things!"""
    if user_id == "me":
        user_id = user.id

    if user.id != user_id and not user.is_admin:
        raise PERMISSION_DENIED

    if user.id != user_id:
        user = users.find(user_id)

    if user.username != body.username and users.find_by("username")(body.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is not available.",
        )

    email = body.email.lower()

    if user.email != email and users.find_by("email")(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not available.",
        )
    try:
        return users.update(user.id, dict(username=body.username, email=email))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Something went very wrong.",
        )


@users_router.delete("/{user_id}")
def delete_user(
    user: AuthorizedUser,
    users: Annotated[Users, Depends(Users.dependency)],
    user_id: int | Literal["me"],
    response: Response,
):
    if user_id == "me":
        user_id = user.id

    if user.id != user_id and not user.is_admin:
        raise PERMISSION_DENIED

    users.delete(user_id)
    response.delete_cookie("mvmcryptionauthtoken", secure=False, httponly=True)
    response.status_code = status.HTTP_204_NO_CONTENT


@users_router.get("/{user_id}")
def user_detail(
    user: AuthorizedUser,
    users: Annotated[Users, Depends(Users.dependency)],
    user_id: int | Literal["me"],
):
    if user_id == "me":
        user_id = user.id

    if user.id != user_id and not user.is_admin:
        raise PERMISSION_DENIED
    if record := users.find(user_id):
        return record
    raise not_found(Users.model)
