from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from apps.users.models import User
from config.settings import settings
from config.db.db_helper import db_helper
from apps.users import crud as crud_users
from apps.auth.services import auth_service
from apps.email.services import send_login_email
from .schemas import ResponseLogin, RequestCompleteLogin, ResponseLogout, TokenSchema, RequestEmail

router = APIRouter()


@router.post("/request-login", response_model=ResponseLogin)
async def request_login(
    email_data: RequestEmail,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    await crud_users.create_user_by_email(email_data.email, session)
    login_token = await auth_service.create_login_token(data={"sub": email_data.email})
    login_link = f"{settings.frontend_url}/complete-login/{login_token}"

    # Send email with login link
    await send_login_email(email_data.email, login_link)

    return {
        "error": False,
        "title": "Success",
        "mail": email_data.email,
        "message": f"Login link sent to your email: {email_data.email}."
    }


@router.post("/complete-login", response_model=TokenSchema)
async def complete_login(
    token: RequestCompleteLogin,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    email = await auth_service.decode_login_token(token.login_token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login token")

    user = await crud_users.get_user_by_email_and_confirm(email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await crud_users.update_token(user, refresh_token, session)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(token: str = Depends(auth_service.oauth2_scheme), session: AsyncSession = Depends(db_helper.session_getter)):
    email = await auth_service.decode_refresh_token(token)
    user = await crud_users.get_user_by_email(email, session)
    if user.refresh_token != token:
        await crud_users.update_token(user, None, session)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await crud_users.update_token(user, refresh_token, session)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/logout", response_model=ResponseLogout)
async def logout(
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    await crud_users.update_token(user, None, session)
    return {"message": "Logged out successfully"}
