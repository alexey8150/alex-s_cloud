from typing import Annotated
import aiohttp
from aiohttp import FormData
from fastapi import APIRouter, Depends, Response, Request
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c

from fastui.components.display import DisplayLookup
from fastui.events import AuthEvent, GoToEvent
import cloud_ui.form
from fastui.forms import fastui_form

from cloud_ui.schemas import LoginForm, UserConfirmationEmail, ConfirmationCode, Upload_File, UserFiles
from cloud_ui.ui_auth import User_UI
from settings import BASE_URL
from tasks.tasks import send_user_password
from cloud_ui.responses import ERROR_RESPONSE
from cloud_ui.utils import get_random_pass, is_authorized

cloud_ui_router = APIRouter(include_in_schema=False)


@cloud_ui_router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def main_page() -> [AnyComponent]:
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Добро пожаловать в облачное хранилище Alex\'s cloud.', level=2),
                c.Button(text='Войти', on_click=GoToEvent(url='/sign_in')),
                c.Heading(text=' ', level=2),
                c.Button(text='Регистрация', on_click=GoToEvent(url='/registration')),
            ]
        ),
    ]


@cloud_ui_router.get("/api/sign_in", response_model=FastUI, response_model_exclude_none=True)
async def sign_in_page(user: Annotated[User_UI, Depends(User_UI.from_request)]) -> [AnyComponent]:
    if user:
        return [c.FireEvent(event=GoToEvent(url='/profile'))]
    return [
        c.Page(
            components=[
                c.Heading(text='Sign in', level=2),
                c.ModelForm(
                    model=LoginForm,
                    display_mode='page',
                    submit_url='/api/auth/sign_in'
                ),
            ]
        ),
    ]


@cloud_ui_router.post("/api/auth/sign_in", response_model=FastUI, response_model_exclude_none=True)
async def sign_in(form: Annotated[LoginForm, fastui_form(LoginForm)], response: Response) -> list[AnyComponent]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{BASE_URL}/api/auth/login',
                                    data={'username': form.username,
                                          'password': form.password.get_secret_value()}) as result:
                auth_token = result.cookies.get('auth_token').value

                response.set_cookie(key='auth_token', value=auth_token, domain='localhost', httponly=True,
                                    max_age=3600,
                                    path='/', samesite='lax', secure=True)

                user = User_UI(email=form.username, extra={})
                responses = {204: [
                    c.Page(
                        components=[
                            c.FireEvent(event=AuthEvent(token=user.encode_token(), url='/profile'))
                        ]
                    ),
                ],
                    400: [
                        c.Page(
                            components=[
                                c.Heading(text='Неверно введен логин и\или пароль', level=4),
                                c.ModelForm(
                                    model=LoginForm,
                                    display_mode='page',
                                    submit_url='/api/auth/sign_in'
                                ),
                            ]
                        ),
                    ]}
                return responses[result.status]
    except (aiohttp.ClientError, KeyError):
        return ERROR_RESPONSE


@cloud_ui_router.get("/api/profile", response_model=FastUI, response_model_exclude_none=True)
@is_authorized
async def profile_page(user: Annotated[User_UI, Depends(User_UI.from_request)]) -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text=f'Hello, {user.email}', level=2),
                c.Button(text='Мои файлы', on_click=GoToEvent(url='/user_files')),
                c.Heading(text=' ', level=2),
                c.Button(text='Выйти', on_click=GoToEvent(url='/logout')),
                c.ModelForm(
                    model=Upload_File,
                    display_mode='page',
                    submit_url='/api/upload_file'
                ),
            ]
        ),
    ]


@cloud_ui_router.get("/api/user_files", response_model=FastUI, response_model_exclude_none=True)
@is_authorized
async def profile_page(user: Annotated[User_UI, Depends(User_UI.from_request)], request: Request) -> list[AnyComponent]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{BASE_URL}/api/cloud/', cookies=request.cookies) as result:
                files = (await result.json())['data']
                files = [UserFiles(file_id=file['file_id'], filename=file['filename']) for file in files]
                if result.status != 200:
                    return ERROR_RESPONSE
                return [
                    c.Page(
                        components=[
                            c.Heading(text='Ваши файлы.'),
                            c.Table(
                                data=files,
                                columns=[
                                    DisplayLookup(field='filename'),
                                    DisplayLookup(field='download_link',
                                                  on_click=GoToEvent(
                                                      url='http://localhost:8000/api/cloud/download_file?file_id={file_id}')),
                                ],
                            ),
                            c.Button(text='Вернутся в профиль', on_click=GoToEvent(url='/profile'))
                        ]
                    ),
                ]
    except aiohttp.ClientError:
        return ERROR_RESPONSE


@cloud_ui_router.get("/api/registration", response_model=FastUI, response_model_exclude_none=True)
@is_authorized
async def registration_page(user: Annotated[User_UI, Depends(User_UI.from_request)]) -> [AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text='Registration', level=2),
                c.ModelForm(
                    model=UserConfirmationEmail,
                    display_mode='page',
                    submit_url='/api/confirm_email'
                ),
            ]
        ),
    ]


@cloud_ui_router.post("/api/confirm_email", response_model=FastUI, response_model_exclude_none=True)
async def confirm_email(form: Annotated[UserConfirmationEmail, fastui_form(UserConfirmationEmail)],
                        response: Response) -> [AnyComponent]:
    response.set_cookie(key='email_user', value=form.email)
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{BASE_URL}/api/auth/send_code',
                                json={"email": form.email}) as result:
            if result.status != 200:
                return [c.Page(
                    components=[
                        c.Heading(text=f'Произошла ошибка отправки кода подтверждения, пожалуйста попробуйте позже.',
                                  level=3),
                        c.Button(text='Вернутся на главную', on_click=GoToEvent(url='/')),
                    ]
                ),
                ]

    return [
        c.Heading(text=f'1.Пожалуйста введите код подтверждения отправленный на адрес {form.email}', level=3),
        c.ModelForm(
            model=ConfirmationCode,
            display_mode='page',
            submit_url='/api/set_password'
        ),
    ]


@cloud_ui_router.post("/api/set_password", response_model=FastUI, response_model_exclude_none=True)
async def set_password(form: Annotated[ConfirmationCode, fastui_form(ConfirmationCode)], request: Request) -> [
    AnyComponent]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{BASE_URL}/api/auth/check_code',
                                    json={"email": request.cookies.get('email_user'),
                                          'code': form.confirm_code}) as result:
                if not (await result.json())['result']:
                    return [
                        c.Heading(text=f'Введен неверный код, попробуйте еще раз.',
                                  level=3),
                        c.ModelForm(
                            model=ConfirmationCode,
                            display_mode='page',
                            submit_url='/api/set_password'
                        ),
                    ]
            password = get_random_pass()

            async with session.post(f'http://{BASE_URL}/api/auth/register',
                                    json={
                                        "email": request.cookies.get('email_user'),
                                        "password": password,
                                        "is_active": False,
                                        "is_superuser": False,
                                        "is_verified": False,
                                        "username": request.cookies.get('email_user')
                                    }) as result:
                if result.status == 201:
                    send_user_password.delay(request.cookies.get('email_user'), password)
                    return [
                        c.Page(
                            components=[
                                c.Heading(
                                    text=f'Войдите в систему. Пароль для входа отправлен на электронную почту {request.cookies.get("email_user")}',
                                    level=2),
                                c.Button(text='Войти', on_click=GoToEvent(url='/sign_in')),
                            ]
                        ),
                    ]
                elif result.status == 400:
                    return [
                        c.Page(
                            components=[
                                c.Heading(text='Пользователь с введенным адресом электронной почты уже существует.',
                                          level=4),
                            ]
                        ),
                    ]
    except aiohttp.ClientError:
        return ERROR_RESPONSE


@cloud_ui_router.get("/api/logout", response_model=FastUI, response_model_exclude_none=True)
async def logout(request: Request) -> [AnyComponent]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{BASE_URL}/api/auth/logout', cookies=request.cookies) as result:
                if result.status not in (200, 204):
                    return ERROR_RESPONSE
                return [c.FireEvent(event=AuthEvent(token=False, url='/'))]
    except aiohttp.ClientError:
        return ERROR_RESPONSE


@cloud_ui_router.post("/api/upload_file", response_model=FastUI, response_model_exclude_none=True)
async def confirm_email(form: Annotated[Upload_File, fastui_form(Upload_File)], request: Request) -> [AnyComponent]:
    try:
        async with aiohttp.ClientSession() as session:
            form_data = FormData()
            form_data.add_field(name='file', value=form.file.file.read(),
                                filename=form.file.filename,
                                content_type=form.file.content_type)
            async with session.post(f'http://{BASE_URL}/api/cloud/',
                                    data=form_data, cookies=request.cookies) as result:
                if result.status != 201:
                    return ERROR_RESPONSE

                return [c.FireEvent(event=GoToEvent(url='/user_files'))]
    except aiohttp.ClientError:
        return ERROR_RESPONSE


@cloud_ui_router.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Alex\'s cloud'))
