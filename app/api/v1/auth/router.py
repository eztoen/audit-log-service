from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import get_db

from .schemas import RegisterSchema
from .service import register_user

router = APIRouter(tags=['Auth'])

@router.post('/register')
async def register(
    request:  Request,
    new_user: RegisterSchema,
    session:  AsyncSession = Depends(get_db)
):
    return await register_user(
        new_user=new_user,
        session=session
    )