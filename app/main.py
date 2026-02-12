from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine

app = FastAPI()

@app.get('/')
async def test():
    return {'hello': 'world'}