from app.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    __tablename__ = 'Users'
    
    id:       Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    name:     Mapped[str] = mapped_column()
    surname:  Mapped[str] = mapped_column()
    email:    Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()