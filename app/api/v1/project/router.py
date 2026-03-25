from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import get_db
from app.services.security.jwt import jwt_service

from .schemas import ProjectCreateSchema, ProjectReadSchema
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
    
@router.get('/', response_model=list[ProjectReadSchema])
async def get_projects(
    limit:   int = Query(10, ge=1, le=50),
    offset:  int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db),
    user_id: int = Depends(jwt_service.get_user_id)
):
    return await service.get_projects(
        session=session,
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    
@router.get('/search', response_model=list[ProjectReadSchema])
async def get_projects(
    q:       str = Query(...),
    session: AsyncSession = Depends(get_db),
    user_id: int = Depends(jwt_service.get_user_id)
):
    return await service.get_projects_by_search(
        session=session,
        user_id=user_id,
        q=q
    )