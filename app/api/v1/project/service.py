from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import ProjectCreateSchema
from app.core.models import Projects
from app.services.security.hashing import hash_value, verify_value
from app.services.security.api_key import generate_api_key, split_api_key


async def create_project(
    new_project: ProjectCreateSchema,
    session: AsyncSession,
    user_id: int
):
    raw_key = generate_api_key()
    
    public_part, secret_part = split_api_key(raw_key)
    hashed_secret = hash_value(secret_part)
    
    project = Projects(
        name = new_project.name,
        public_key=public_part,
        hashed_key=hashed_secret,
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
            detail='Project already exists'
        )
    
    return project, raw_key

async def get_projects(
    session: AsyncSession,
    user_id: int,
    limit: int,
    offset: int
):
    result = await session.execute(
        select(Projects)
        .where(Projects.user_id == user_id)
        .order_by(Projects.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    projects = result.scalars().all()
    
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no projects yet. Let's do it!"
        )
    
    return projects

async def get_projects_by_search(
    session: AsyncSession,
    user_id: int,
    q: str
):
    q = q.strip()
    
    if not q:
        return []
    
    stmt = (
        select(Projects)
        .where(
            Projects.user_id == user_id,
            Projects.name.ilike(f'%{q}%')
        )
        .limit(20)
    )
    
    result = await session.execute(stmt)
    return result.scalars().all()