from typing import Optional

from pydantic import BaseModel, constr


class AccountCreatesSchema(BaseModel):
    username: Optional[constr(min_length=8, max_length=32)]  # type: ignore
    password: Optional[constr(min_length=16, max_length=64)]  # type: ignore


class AccountUpdateSchema(BaseModel):
    country: Optional[str]
    job: Optional[str]
    company: Optional[str]
    age: Optional[int]
