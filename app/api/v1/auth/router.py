from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import get_db

from .schemas import RegisterSchema, LoginSchema
from .service import register_user, login_user

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
    
@router.post('/login')
async def login(
    request: Request,
    user: LoginSchema,
    session: AsyncSession = Depends(get_db)
):
    return await login_user(
        user=user,
        session=session
    )