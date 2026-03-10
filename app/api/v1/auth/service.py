from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from .schemas import RegisterSchema, LoginSchema
from app.core.models import Users
from app.services.security.hashing import hash_value, verify_value
from app.services.security.jwt import jwt_service

async def get_exist_user(
    session: AsyncSession,
    email: str
) -> Users | None:
    
    result = await session.execute(
        select(Users).where(
            Users.email == email
        )
    )
    
    return result.scalar_one_or_none()

async def register_user(
    new_user: RegisterSchema,
    session: AsyncSession
) -> Users:
    
    user = await get_exist_user(
        session=session,
        email=new_user.email
    )
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The email you have provided is already associated with an account.'
        )
        
    user = Users(
        username = new_user.username,
        first_name = new_user.first_name,
        last_name = new_user.last_name,
        email = new_user.email,
        password = hash_value(new_user.password)
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
    user: LoginSchema,
    session: AsyncSession
):
    exist_user = await get_exist_user(
        session=session,
        email=user.email
    )
    
    if not exist_user or not verify_value(user.password, exist_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials. Please try again'
        )
        
    access_token = jwt_service.create_access_token({'sub': str(exist_user.id)})
    
    return {
        'success': True,
        'detail': 'You have successfully logged into your account',
        'access_token': access_token,
        'type': 'bearer'
    }