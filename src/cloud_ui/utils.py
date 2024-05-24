import functools
from string import ascii_letters
from random import choice
from typing import Annotated
from fastapi import Depends
from fastapi.responses import Response
from fastui import components as c
from fastui.events import GoToEvent


from cloud_ui.ui_auth import User_UI


def get_random_pass():
    password = ''
    for _ in range(10):
        password += choice(ascii_letters)

    return password


def is_authorized(func):
    @functools.wraps(func)
    async def wrapper(user: Annotated[User_UI, Depends(User_UI.from_request)], *args, **kwargs):
        if not user:
            return [c.FireEvent(event=GoToEvent(url='/sign_in'))]
        response: Response = await func(user, *args, **kwargs)
        return response

    return wrapper
