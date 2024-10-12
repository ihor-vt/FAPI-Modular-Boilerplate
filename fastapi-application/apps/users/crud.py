from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UpdateUser


async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User | None]:
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_email_and_confirm(email: str, session: AsyncSession) -> Optional[User | None]:
    result = await session.execute(select(User).filter(User.email == email))
    user = result.scalars().first()

    if user and not user.is_verified:
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_verified=True)
        )
        await session.commit()

        user.is_verified = True

    return user


async def create_user_by_email(email: EmailStr, session: AsyncSession) -> None:
    # try:
    #     db_user = User(email=email)
    #     session.add(db_user)
    #     await session.commit()
    # except IntegrityError:
    #     await session.rollback()
    # SQlAlchemy is too slow
    query = """
        INSERT INTO users (email)
        VALUES (:email)
        ON CONFLICT (email) DO NOTHING;
    """

    try:
        await session.execute(query, {"email": email})
        await session.commit()
    except IntegrityError:
        await session.rollback()


async def update_token(user: User, token: str | None, session: AsyncSession) -> None:
    user.refresh_token = token
    await session.commit()


async def update_user(user: User, updated_data: UpdateUser, session: AsyncSession) -> User:
    update_fields = updated_data.dict(exclude_unset=True)

    if update_fields:
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(**update_fields)
            .execution_options(synchronize_session="fetch")
        )

        await session.execute(stmt)
        await session.commit()

        result = await session.execute(select(User).where(User.id == user.id))
        updated_user = result.scalar_one_or_none()

        return updated_user

    return user
