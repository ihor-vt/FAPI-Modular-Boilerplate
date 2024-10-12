from pydantic import BaseModel, EmailStr, UUID4


# User
class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    first_name: str | None
    last_name: str | None


class UpdateUser(BaseModel):
    first_name: str
    last_name: str
