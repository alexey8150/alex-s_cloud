from fastapi import FastAPI
from sqladmin import Admin, ModelView
import aioredis

from auth.base_config import auth_backend, fastapi_users
from auth.router import router_confirmation_email
from auth.schemas import UserRead, UserCreate
from auth_admin import authentication_backend
from database import engine

from auth.models import User
from cloud.router import router_files_of_user
from cloud_ui.router import cloud_ui_router

app = FastAPI(title='Alex\'s Cloud')


"""
ROUTERS
"""

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["Auth"],
)

app.include_router(router_confirmation_email)

app.include_router(router_files_of_user)

app.include_router(cloud_ui_router)

"""
ADMIN PANEL
"""

admin = Admin(app, engine, authentication_backend=authentication_backend)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.registered_at, User.is_active, User.is_verified,
                   User.is_superuser]


admin.add_view(UserAdmin)
