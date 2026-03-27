from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import ProjectCreateSchema, ProjectChangeNameSchema
from app.core.models import Projects
from app.services.security.hashing import hash_value
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
    
    try:
        session.add(project)
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
        .where(
            Projects.user_id == user_id,
            Projects.is_deleted == False
        )
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

async def get_project_by_id(
    session: AsyncSession,
    user_id: int,
    project_id: int
):
    result = await session.execute(
        select(Projects)
        .where(
            Projects.user_id == user_id,
            Projects.id == project_id,
            Projects.is_deleted == False
        )
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project

async def get_projects_by_search(
    session: AsyncSession,
    user_id: int,
    q: str,
    limit: int,
    offset: int
):
    q = q.strip()
    
    if not q:
        return []
    
    stmt = (
        select(Projects)
        .where(
            Projects.user_id == user_id,
            Projects.is_deleted == False,
            Projects.name.ilike(f'%{q}%')
        )
        .limit(limit)
        .offset(offset)
        .limit(20)
    )
    
    result = await session.execute(stmt)
    return result.scalars().all()

async def change_project_name(
    session: AsyncSession,
    user_id: int,
    project_id: int,
    data: ProjectChangeNameSchema
):
    stmt = (
        update(Projects)
        .where(
            Projects.user_id == user_id,
            Projects.id == project_id,
            Projects.is_deleted == False
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Projects)
    )
    
    try:
        result = await session.execute(stmt)
        project = result.scalar_one_or_none()
    
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project not found'
            )
        await session.commit()
        
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Project with this name already exists'
        )     
        
    return project

async def delete_project(
    session: AsyncSession,
    user_id: int,
    project_id: int
) -> None:
    
    stmt = (
        update(Projects)
        .where(
            Projects.id == project_id,
            Projects.user_id == user_id,
            Projects.is_deleted == False
        )
        .values(
            is_deleted = True
        )
        .returning(Projects.id)
    )
    
    try:
        result = await session.execute(stmt)
        deleted_project = result.scalar_one_or_none()
        
        if not deleted_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project not found'
            )
        
        await session.commit()
        
    except SQLAlchemyError:
        await session.rollback()
        raise