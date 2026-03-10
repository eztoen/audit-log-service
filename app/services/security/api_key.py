import secrets
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Projects

from app.services.security.hashing import hash_value, verify_value

def generate_api_key() -> str:
    prefix = 'sk_live'
    public_part = secrets.token_hex(8)
    secret_part = secrets.token_hex(24)
    
    return f'{prefix}{public_part}{secret_part}'

def split_api_key(raw_key: str) -> tuple[str, str]:
    key = raw_key.repalce('sk_live_', '')
    public_part = key[:16]
    secret_part = key[16:]
    return public_part, secret_part

async def authentificate_api_key(db: AsyncSession, raw_key: str):
    if not raw_key.startswith('sk_live_'):
        return None
    
    public_part, secret_part = split_api_key(raw_key)
    
    result = await db.execute(
        select(Projects).where(Projects.public_key == public_part)
    )
    
    project = result.scalar_one_or_none()
    
    if not project:
        return None
    
    incoming_hash = hash_value(secret_part)
    
    if not verify_value(incoming_hash, Projects.hashed_key):
        return None
    
    return project