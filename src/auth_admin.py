from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fastapi_users.password import PasswordHelper

from auth.models import User
from database import async_session_maker
from settings import SECRET_AUTH


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        password_helper = PasswordHelper()
        session = async_session_maker()

        query = select(User).where(User.username == username)
        result = await session.execute(query)
        result = result.all()
        user = result[0][0]

        verified, updated_password_hash = password_helper.verify_and_update(password, user.hashed_password)

        if not verified:
            return False
        request.session.update({"token": "..."})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


authentication_backend = AdminAuth(secret_key=SECRET_AUTH)
