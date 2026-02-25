from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.models import db_helper
from app.core.models import Base

#routers
from app.api.v1.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print('🔴 TABLES:', Base.metadata.tables)
        
    yield
        
    await conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)