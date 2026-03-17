from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import get_db
from app.services.security.jwt import jwt_service

from .schemas import ProjectCreateSchema
from . import service


router = APIRouter(prefix='/projects', tags=['Projects'])

@router.post('/create')
async def create_project(
    new_project: ProjectCreateSchema,
    session: AsyncSession = Depends(get_db),
    user_id: int = Depends(jwt_service.get_user_id)
):
    return await service.create_project(
        new_project=new_project,
        session=session,
        user_id=user_id
    )