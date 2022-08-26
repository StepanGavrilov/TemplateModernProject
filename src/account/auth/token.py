import jwt

from datetime import datetime, timedelta

from account.auth.secret import SECRET_KEY, ALGORITHM  # type: ignore


def create_access_token(
        sub: str,
        username: str,
        expires_delta: timedelta | None = None
):
    """
    create access token
    data keys: exp, sub, iss
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data = {
        "iss": "templatemodernproject",
        "exp": expire,
        "sub": sub,
        "username": username,
    }

    encoded_jwt = jwt.encode(
        data,
        SECRET_KEY,  # type: ignore
        algorithm=ALGORITHM
    )
    return encoded_jwt
