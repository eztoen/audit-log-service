from distutils.log import Log

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from app.core.models import Users
from .schemas import LogCreateSchema

async def create_log(
    log: LogCreateSchema,
    user_id: int,
    session: AsyncSession
):
    if user_id:
        user = await session.get(Users, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    log_obj = Log(
        ...
    )



    await log_service.create(log)