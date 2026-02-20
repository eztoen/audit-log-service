from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import RegisterSchema
from app.db.models.SQLAlchemy.users import Users

async def register_user(
    new_user: RegisterSchema,
    session: AsyncSession
):
    stmt = select(Users).where(Users.email==new_user.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The email you have provided is already associated with an account'
        )
        
    user = Users(
        username = new_user.username,
        name = new_user.name,
        surname = new_user.surname,
        email = new_user.email,
        password = new_user.password
    )
    session.add(user)
    
    try:
        await session.commit()
        await session.refresh()
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The username already exists'
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='You have successfully registered.'
        )