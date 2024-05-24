import aioredis

from fastapi import APIRouter, HTTPException
from auth.schemas import UserConfirmEmail, CheckConfirmCode
from tasks.tasks import send_confirmation_email
from auth.utils import get_confirm_code

router_confirmation_email = APIRouter(prefix="/api/auth", tags=["Auth"])

"""
EVENTS
"""
redis: aioredis.Redis


@router_confirmation_email.on_event('startup')
async def startup_event():
    global redis
    redis = await aioredis.Redis(host='localhost', port=6379)


@router_confirmation_email.on_event('shutdown')
async def shutdown_event():
    global redis
    await redis.close()


"""
END-POINTS
"""


@router_confirmation_email.post('/send_code')
async def send_code(user_email: UserConfirmEmail):
    try:
        confirm_code = get_confirm_code()
        await redis.set(user_email.email, confirm_code, ex=60)
        print(await redis.get(user_email.email))
        send_confirmation_email.delay(user_email.email, confirm_code)
        return {'status': 'mail was send'}
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_confirmation_email.post('/check_code')
async def check_code(data: CheckConfirmCode):
    try:
        confirm_code = await redis.get(data.email)
        result = data.code == confirm_code.decode()
        if result:
            await redis.set(data.email, 'true', ex=300)
        return {'result': result}
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
