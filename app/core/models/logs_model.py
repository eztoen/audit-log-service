from datetime import UTC, datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base

class Logs(Base):
    __tablename__ = 'logs'
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    user_id:    Mapped[int] = mapped_column(ForeignKey('projects.id'))
    level:      Mapped[str] = mapped_column(String(20))
    message:    Mapped[str]
    timestamp:  Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))