from datetime import UTC, datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base

class Project(Base):
    __tablename__ = 'projects'
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    name:       Mapped[str] = mapped_column(String(100))
    api_key:    Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id:    Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))