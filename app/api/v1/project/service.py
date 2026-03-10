from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import ProjectCreateSchema
from app.core.models import Projects
from app.services.security.hashing import hash_value, verify_value
from app.services.security.api_key import generate_api_key, split_api_key

async def get_exist_project(
    session: AsyncSession,
    user_id: int,
    name: str
) -> Projects | None:
    
    result = await session.execute(
        select(Projects).where(
            Projects.user_id == user_id,
            Projects.name == name
        )
    )
    
    return result.scalar_one_or_none()

async def create_project(
    new_project: ProjectCreateSchema,
    session: AsyncSession,
    user_id: int,
    name: str
):
    raw_key= generate_api_key()
    
    public_part, secret_part = split_api_key(raw_key)
    hashed_secret = hash_value(secret_part)
    
    project = await get_exist_project(
        session=session,
        user_id=user_id,
        name=name
    )
    
    if project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The project you provided is already associated to this account.'
        )
        
    project = Projects(
        name = new_project.name,
        public_key=public_part,
        hashed_secret=hashed_secret,
        user_id=user_id
        
    )
    session.add(project)
    
    try:
        await session.commit()
        await session.refresh(project)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='A project with this name already exists'
        )
    
    return project, raw_key