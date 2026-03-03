from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import ProjectCreateSchema
from app.core.models import Projects

async def get_exist_project(
    session: AsyncSession,
    user_id: int,
    name: str
) -> bool:
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
    project = await get_exist_project(
        session=session,
        user_id=user_id,
        name=name
    )