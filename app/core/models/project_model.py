from datetime import date

from sqlalchemy import Boolean, String, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base

class Projects(Base):
    __tablename__ = 'projects'
    
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uniq_user_project_name'),
)
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    name:       Mapped[str] = mapped_column(String(100))
    public_key: Mapped[str] = mapped_column(String(16), index=True)
    hashed_key: Mapped[str] = mapped_column(String(100))
    user_id:    Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[date] = mapped_column(Date)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)