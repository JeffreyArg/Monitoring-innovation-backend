from sqlalchemy import String, Boolean, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    was_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    created_at: Mapped[str] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[str] = mapped_column(server_default=text("now()"))
