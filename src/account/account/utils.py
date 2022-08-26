from typing import Optional, NoReturn
from aioredis import Redis
from sqlalchemy import select, delete, update
from sqlalchemy.engine import ScalarResult

from account.models.account import Account  # type: ignore
from sqlmodel.ext.asyncio.session import AsyncSession


async def check_account_existence(
        username: str,
        redis_client: Redis,
) -> bool:
    """
    Check if account exists in redis, return True or False,
    used only in endpoints.
    """

    account_exists: str | None = await redis_client.get(
        username.lower(),
    )
    if not isinstance(account_exists, str):
        return False
    return account_exists.lower() == username.lower()


async def get_account_from_db(
        username: str,
        session: AsyncSession,
) -> Optional[Account]:
    """
    Get user from database, return object
    if exists. Used without JWT
    """

    stmt = select(Account).where(Account.username == username)
    account_result: ScalarResult = await session.scalars(stmt)
    account: Optional[Account] = account_result.one_or_none()
    return account


async def delete_user_from_db(
        session: AsyncSession,
        redis_client: Redis,
        account_id: str,
        username: str

) -> bool:
    """
    Deletes account from database.
    In this method we use functionality with redis-check
    account for username and if it exists delete account from
    database and then from redis and return 204 code,
    else if account not exists in redis return error with code
    200.
    """

    account_exists: bool = await check_account_existence(
        username=username,
        redis_client=redis_client
    )
    if not account_exists:
        return False

    stmt = delete(Account).where(Account.id == account_id)
    await session.execute(stmt)
    await session.commit()
    await redis_client.delete(username.lower())
    return True


async def get_user_from_db_by_id(
        username: str,
        session: AsyncSession,
        redis_client: Redis,
        account_id: str
) -> Account | None:
    """
    redis+postgres.
    For account select used account.id with index
    Used ONLY with JWT Token!
    """

    account_exists: bool = await check_account_existence(
        username=username,
        redis_client=redis_client
    )
    if not account_exists:
        return None

    stmt = select(Account).where(Account.id == account_id)
    account_result: ScalarResult = await session.scalars(stmt)
    account: Optional[Account] = account_result.one_or_none()
    return account


async def update_account_data(  # type: ignore
        update_schema: dict,
        session: AsyncSession,
        account_id: str
) -> NoReturn:
    """
    Update account from
    account update schema.
    """

    update_schema = {
        k: v for k, v in
        update_schema.items()
        if v is not None
    }

    stmt = update(Account).where(Account.id == account_id).values(
        **update_schema
    )
    await session.execute(stmt)
    await session.commit()
