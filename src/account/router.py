from fastapi import APIRouter

from account.account_urls import account_router  # type: ignore

user_router = APIRouter()
user_router.include_router(account_router)
