from datetime import UTC, datetime

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base

class Projects(Base):
    __tablename__ = 'projects'
    
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uniq_user_project_name'),
)
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    name:       Mapped[str] = mapped_column(String(100))
    api_key:    Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id:    Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))