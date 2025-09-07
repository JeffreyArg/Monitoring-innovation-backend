from sqlalchemy import String, Boolean, Integer, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    locality_id: Mapped[int] = mapped_column(ForeignKey("localities.id", ondelete="RESTRICT"), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="RESTRICT"), nullable=False)
    applicant_name: Mapped[str] = mapped_column(String(150), nullable=False)
    was_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    created_at: Mapped[str] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[str] = mapped_column(server_default=text("now()"))

    locality = relationship("Locality")
    brand = relationship("Brand")
