import logging

import uvicorn

from config.settings import settings
from config.main import create_app


logging.basicConfig(
    # level=logging.INFO
    format=settings.logging.log_format,
)

main_app = create_app()


if __name__ == "__main__":
    # For local development
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_level=settings.logging.log_level
    )

    # For production
    # from config.gunicorn import Application, get_app_options

    # Application(
    #     application=main_app,
    #     options=get_app_options(
    #         host=settings.gunicorn.host,
    #         port=settings.gunicorn.port,
    #         timeout=settings.gunicorn.timeout,
    #         workers=settings.gunicorn.workers,
    #         log_level=settings.logging.log_level,
    #     ),
    # ).run()
