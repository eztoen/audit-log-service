from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import RegisterSchema
from app.core.models import Users
from app.services.security.hashing import hash_password, verify_password

async def get_user(
    session: AsyncSession,
    email: str
) -> Users | None:
    stmt = select(Users).where(Users.email == email)
    result = await session.execute(stmt)    
    
    return result.scalar_one_or_none()


async def register_user(
    new_user: RegisterSchema,
    session: AsyncSession
) -> Users:
    
    user = await get_user(
        session=session,
        email=new_user.email
    )
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The email you have provided is already associated with an account'
        )
        
    user = Users(
        username = new_user.username,
        first_name = new_user.first_name,
        last_name = new_user.last_name,
        email = new_user.email,
        password = hash_password(new_user.password)
    )
    session.add(user)
    
    try:
        await session.commit()
        await session.refresh(user)
        
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The username already exists'
        )
    return user
        
async def login_user(
    new_user: RegisterSchema,
    session: AsyncSession
):
    user = await get_user(
        session=session,
        email=new_user.email
    )