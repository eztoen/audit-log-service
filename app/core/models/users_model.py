from app.core.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    id:         Mapped[int] = mapped_column(primary_key=True)
    username:   Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name:  Mapped[str] = mapped_column()
    email:      Mapped[str] = mapped_column(unique=True)
    password:   Mapped[str] = mapped_column()