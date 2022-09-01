# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.user import User


router = APIRouter()


@router.post(
    "/user",
    responses={
        200: {"model": User, "description": "successful operation"},
    },
    tags=["user"],
    summary="Create user",
    response_model_by_alias=True,
)
async def create_user(
    user: User = Body(None, description="Created user object"),
) -> User:
    """This can only be done by the logged in user."""
    ...


@router.post(
    "/user/createWithList",
    responses={
        200: {"model": User, "description": "Successful operation"},
        200: {"description": "successful operation"},
    },
    tags=["user"],
    summary="Creates list of users with given input array",
    response_model_by_alias=True,
)
async def create_users_with_list_input(
    user: List[User] = Body(None, description=""),
) -> User:
    """Creates list of users with given input array"""
    ...


@router.delete(
    "/user/{username}",
    responses={
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
    tags=["user"],
    summary="Delete user",
    response_model_by_alias=True,
)
async def delete_user(
    username: str = Path(None, description="The name that needs to be deleted"),
) -> None:
    """This can only be done by the logged in user."""
    ...


@router.get(
    "/user/{username}",
    responses={
        200: {"model": User, "description": "successful operation"},
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
    tags=["user"],
    summary="Get user by user name",
    response_model_by_alias=True,
)
async def get_user_by_name(
    username: str = Path(None, description="The name that needs to be fetched. Use user1 for testing. "),
) -> User:
    """"""
    ...


@router.get(
    "/user/login",
    responses={
        200: {"model": str, "description": "successful operation"},
        400: {"description": "Invalid username/password supplied"},
    },
    tags=["user"],
    summary="Logs user into the system",
    response_model_by_alias=True,
)
async def login_user(
    username: str = Query(None, description="The user name for login"),
    password: str = Query(None, description="The password for login in clear text"),
) -> str:
    """"""
    ...


@router.get(
    "/user/logout",
    responses={
        200: {"description": "successful operation"},
    },
    tags=["user"],
    summary="Logs out current logged in user session",
    response_model_by_alias=True,
)
async def logout_user(
) -> None:
    """"""
    ...


@router.put(
    "/user/{username}",
    responses={
        200: {"description": "successful operation"},
    },
    tags=["user"],
    summary="Update user",
    response_model_by_alias=True,
)
async def update_user(
    username: str = Path(None, description="name that need to be deleted"),
    user: User = Body(None, description="Update an existent user in the store"),
) -> None:
    """This can only be done by the logged in user."""
    ...
