from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from app.core.config import settings

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = True):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

db_helper = DatabaseHelper(
    url=settings.db_url,
)

get_db = db_helper.get_scoped_session