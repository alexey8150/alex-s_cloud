import os
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import unquote_plus

from database import get_async_session
from settings import MEDIA_PATH
from auth.base_config import current_user
from cloud.models import File as UserFiles
from cloud.schemas import UserFiles as UserFilesSchema

router_files_of_user = APIRouter(prefix='/api/cloud', tags=['Cloud'])


@router_files_of_user.post('/')
async def upload_file(file: UploadFile, user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        file.filename = unquote_plus(file.filename)
        stmt = insert(UserFiles).values(filename=file.filename, user_id=user.id)
        await session.execute(stmt)
        await session.commit()

        file_path = f'{MEDIA_PATH}/{user.id}/'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path + file.filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()
        return JSONResponse(content={'status': 'success'}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_files_of_user.get('/')
async def get_files_of_users(user=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(UserFiles).where(UserFiles.user_id == user.id)
        result = await session.execute(query)
        result = result.all()
        content = {'status': 'success',
                   'data': [UserFilesSchema(file_id=result[i][0].id, filename=result[i][0].filename).dict() for i in
                            range(len(result))]}
        return JSONResponse(content=content, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_files_of_user.get('/download_file')
async def get_files_of_users(file_id: int, user=Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(UserFiles).where(UserFiles.user_id == user.id, UserFiles.id == file_id)
        result = await session.execute(query)
        result = result.all()
        file = result[0][0]
        file_path = f'{MEDIA_PATH}/{user.id}/{file.filename}'
        return FileResponse(path=file_path, filename=file.filename, status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
