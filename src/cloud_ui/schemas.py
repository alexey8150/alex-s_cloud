from typing import Annotated


from fastapi import UploadFile
import cloud_ui.form
from fastui.forms import FormFile
from pydantic import BaseModel, EmailStr, SecretStr, Field



class LoginForm(BaseModel):
    username: EmailStr
    password: SecretStr


class UserConfirmationEmail(BaseModel):
    email: EmailStr = Field(description='Enter your email address')


class ConfirmationCode(BaseModel):
    confirm_code: str = Field(description='Enter code')


class Upload_File(BaseModel):
    file: Annotated[UploadFile, FormFile(accept='*/*', max_size=500_000)] = Field(
        description='Загрузите ваш файл.'
    )

class UserFiles(BaseModel):
    file_id: int
    filename: str
    download_link: str = 'Скачать'
