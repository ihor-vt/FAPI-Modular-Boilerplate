import logging
from typing import Annotated
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status

# from src.api.deps import api_router
from config.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI-Modular-Boilerplate",
        description="""FastAPI-Modular-Boilerplate is a powerful starter template
          for developing scalable web applications using FastAPI. Inspired by Django's
          best practices, this template offers a modular structure that ensures
          clear code organization and easy functionality expansion.""",
        version="0.0.1",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        contact={
                "name": "Admin",
                "url": "https://github.com/ihor-vt/FastAPI-Modular-Boilerplate",
                "email": "admin@example.com",
        }
    )

    router = APIRouter()

    @router.get("/healthchecker")
    async def healthchecker(session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ]):
        """Health checker for the API"""
        try:
            result = await session.execute(text("SELECT 1"))
            result = result.fetchone()
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not configured correctly"
                )
            return {"message": "Database connected!"}
        except Exception as e:
            logging.error(f"healthchecker: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connecting to the database")

    # app.include_router(
    #     api_router,
    # )
    # app.include_router(
    #     healthchecker_router,
    # )

    return app
