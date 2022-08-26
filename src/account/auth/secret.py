from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext  # type: ignore

from config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("ACCESS_TOKEN_EXPIRE_MINUTES")
