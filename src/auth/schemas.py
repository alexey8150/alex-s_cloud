from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, ConfigDict, Field


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserConfirmEmail(BaseModel):
    email: EmailStr


class CheckConfirmCode(BaseModel):
    email: EmailStr
    code: str
