from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        yield
        
        await conn.close()

app = FastAPI(lifespan=lifespan)