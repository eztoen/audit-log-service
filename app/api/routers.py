from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import RegisterSchema
from app.models.users import Users

router = APIRouter()

# @router.get('/test')
# async def test(
#     new_user: RegisterSchema,
#     session: AsyncSession
# ):
#     user = Users(
#         username = new_user.username,
#         name = new_user.name,
#         surname = new_user.surname,
#         email = new_user.email,
#         #Without hash cause this is test function
#         password = new_user.password,
#     )
    
#     session.add(user)
    
#     session.commit()