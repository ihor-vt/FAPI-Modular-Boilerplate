from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from config.settings import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail.m_username,
    MAIL_PASSWORD=settings.mail.m_password,
    MAIL_FROM=settings.mail.m_username,
    MAIL_PORT=settings.mail.m_port,
    MAIL_SERVER=settings.mail.m_server,
    MAIL_FROM_NAME="FastAPI Modular Boilerplate",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_login_email(email: str, login_link: str):
    message = MessageSchema(
        subject="Your Login Link",
        recipients=[email],
        body=f"Click this link to log in: {login_link}",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
