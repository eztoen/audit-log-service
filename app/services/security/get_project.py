from fastapi import Header, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import get_db

...