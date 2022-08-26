from typing import Dict

import jwt
import orjson
from datetime import timedelta
from aioredis import Redis

from account.account.utils import (
    check_account_existence, get_account_from_db, delete_user_from_db,
    get_user_from_db_by_id, update_account_data
)  # type: ignore
from account.auth.secret import (
    ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme,
    SECRET_KEY, ALGORITHM
)  # type: ignore
from account.auth.token import create_access_token  # type: ignore
from account.models.schema import (
    AccountCreatesSchema, AccountUpdateSchema
)  # type: ignore
from integrations.redis.redis_storage import init_redis_pool  # type: ignore
from src.database.connection import get_session  # type: ignore
from account.models.account import Account  # type: ignore

from account.auth.password import (
    get_password_hash, verify_password
)  # type: ignore

from fastapi import Depends, Response, status, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

account_router = APIRouter()


@account_router.delete('/account/', tags=['account'])
async def delete_account(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(init_redis_pool)
) -> Response:
    """
    Delete Account.
    Check account for existence
    """

    try:
        payload: Dict[str, str | int] = jwt.decode(
            token,
            SECRET_KEY,  # type: ignore
            algorithms=[ALGORITHM]  # type: ignore
        )
    except jwt.exceptions.ExpiredSignatureError:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=orjson.dumps({"detail": {"message": "Token expired"}})
        )
    except jwt.exceptions.InvalidSignatureError:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=orjson.dumps({"detail": {"message": "Invalid token"}})
        )

    delete_status = await delete_user_from_db(
        session=session,
        redis_client=redis_client,
        account_id=payload.get("sub"),  # type: ignore
        username=payload.get("username"),  # type: ignore
    )

    if not delete_status:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=orjson.dumps({
                "detail": {
                    "message": "Account not deleted"
                }
            })
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@account_router.post('/account/', tags=['account'])
async def create_account(
        account_schema: AccountCreatesSchema,
        session: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(init_redis_pool)
) -> Response:
    """
    1. Validate for username, email and password use
    pydantic schema.
    2. check email in redis, if exists return error else
    creates new account and return jwt.
    :return: Response
    """

    account_exists: bool = await check_account_existence(
        username=account_schema.username,  # type: ignore
        redis_client=redis_client
    )
    if account_exists:
        return Response(
            media_type="application/json",
            status_code=status.HTTP_409_CONFLICT,
            content=orjson.dumps(
                {
                    "detail": {
                        "message": "Account with this username "
                                   "or email already exists."
                    }
                }))

    account = Account(
        username=account_schema.username,
        password=get_password_hash(account_schema.password)  # type: ignore
    )

    session.add(account)
    await session.commit()
    await session.refresh(account)
    await redis_client.set(
        name=account.username.lower(),
        value=account.username  # type: ignore
    )

    access_token: str = create_access_token(
        sub=str(account.id),  # type: ignore
        username=account.username,  # type: ignore
        expires_delta=timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)  # type: ignore
        )  # type: ignore
    )

    return Response(
        media_type="application/json",
        status_code=status.HTTP_201_CREATED,
        content=orjson.dumps({
            "detail": {
                "access_token": access_token
            }
        })
    )


@account_router.post('/account/login/', tags=['account'])
async def login(
        account_schema: AccountCreatesSchema,
        session: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(init_redis_pool)
) -> Response:
    account_exists: bool = await check_account_existence(
        username=account_schema.username,  # type: ignore
        redis_client=redis_client
    )

    if not account_exists:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    account: Account | None = await get_account_from_db(
        username=account_schema.username,  # type: ignore
        session=session,
    )

    if not account:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    password_verified = verify_password(
        plain_password=account_schema.password,  # type: ignore
        hashed_password=account.password  # type: ignore
    )  # type: ignore

    if not password_verified:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token: str = create_access_token(
        sub=str(account.id),  # type: ignore
        username=account.username,  # type: ignore
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES  # type: ignore
        )  # type: ignore
    )

    return Response(
        media_type="application/json",
        status_code=status.HTTP_200_OK,
        content=orjson.dumps({
            "detail": {
                "message": "Authenticated successfully",
                "token": access_token
            }
        })
    )


@account_router.put('/account/', tags=['account'])
async def update_account(
        account_update_schema: AccountUpdateSchema,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(init_redis_pool)
) -> Response:
    try:
        payload: Dict[str, str | int] = jwt.decode(
            token,
            SECRET_KEY,  # type: ignore
            algorithms=[ALGORITHM]  # type: ignore
        )
    except jwt.exceptions.ExpiredSignatureError:
        return Response(
            media_type="application/json",
            status_code=status.HTTP_400_BAD_REQUEST,
            content=orjson.dumps({"detail": {"message": "Token expired"}})
        )
    except jwt.exceptions.InvalidSignatureError:
        return Response(
            media_type="application/json",
            status_code=status.HTTP_400_BAD_REQUEST,
            content=orjson.dumps({"detail": {"message": "Invalid token"}})
        )

    account: Account | None = await get_user_from_db_by_id(
        username=payload.get("username"),  # type: ignore
        account_id=payload.get("sub"),  # type: ignore
        session=session,
        redis_client=redis_client
    )
    if not account:
        return Response(
            media_type="application/json",
            status_code=status.HTTP_404_NOT_FOUND,
            content=orjson.dumps(
                {"detail": {"message": "Account not found."}}
            )
        )

    await update_account_data(
        session=session,
        update_schema=account_update_schema.dict(),
        account_id=account.id  # type: ignore
    )

    return Response(
        media_type="application/json",
        status_code=status.HTTP_200_OK
    )
