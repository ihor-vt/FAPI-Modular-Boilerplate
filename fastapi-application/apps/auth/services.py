import logging
from typing import Optional
from datetime import datetime, timedelta, UTC

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt

from config.settings import settings
from config.db.db_helper import db_helper
from apps.users import crud as crud_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.auth_user.secret_key
    ALGORITHM = settings.auth_user.algorithm

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/request-login")

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = settings.auth_user.expire_access_token
    ) -> str:
        to_encode = data.copy()
        datetime_now = datetime.now(UTC)
        expire = datetime_now + timedelta(seconds=expires_delta)
        to_encode.update(
            {"iat": datetime_now, "exp": expire, "scope": "access_token"}
        )
        return jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = settings.auth_user.expire_refresh_token
    ) -> str:
        to_encode = data.copy()
        datetime_now = datetime.now(UTC)
        expire = datetime_now + timedelta(seconds=expires_delta)
        to_encode.update(
            {"iat": datetime_now, "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def create_login_token(self, data: dict) -> str:
        to_encode = data.copy()
        datetime_now = datetime.now(UTC)
        # Login token expires in 1 hour
        expire = datetime_now + timedelta(hours=1)
        to_encode.update(
            {"iat": datetime_now, "exp": expire, "scope": "login_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY,
                           algorithm=self.ALGORITHM)
        return token

    async def decode_login_token(self, login_token: str) -> str:
        try:
            payload = jwt.decode(
                login_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload.get("scope", "nothing") == "login_token":
                email = payload.get("sub", None)
                if email is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
                return email
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Invalid login token"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login token has expired.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def decode_refresh_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload.get("scope", "nothing") == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError as error:
            logging.error(f"> decode_refresh_token: {error}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(db_helper.session_getter)
    ) -> dict:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[
                self.ALGORITHM])
            email = payload.get("sub")
            if not email or payload.get("scope") != "access_token":
                raise credentials_exception
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise credentials_exception

        user = await crud_users.get_user_by_email(email, session)
        if not user:
            raise credentials_exception
        return user


auth_service = Auth()
