from account.auth.secret import pwd_context  # type: ignore


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
