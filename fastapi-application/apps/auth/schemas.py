from pydantic import BaseModel, EmailStr


class RequestEmail(BaseModel):
    email: EmailStr


class ResponseLogin(BaseModel):
    error: bool = False
    title: str = "Success"
    mail: EmailStr
    message: str = "Login link sent to your email."


class RequestCompleteLogin(BaseModel):
    login_token: str


class ResponseLogout(BaseModel):
    message: str = "Logged out successfully"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
