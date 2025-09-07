from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.entities.brand import Brand

class BrandRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, brand_id: int) -> Optional[Brand]:
        return self.db.get(Brand, brand_id)

    def get_by_name(self, name: str) -> Optional[Brand]:
        stmt = select(Brand).where(Brand.name == name)
        return self.db.scalar(stmt)

    def list(self, include_deleted: bool = False) -> Iterable[Brand]:
        stmt = select(Brand)
        if not include_deleted:
            stmt = stmt.where(Brand.was_deleted.is_(False))
        return self.db.scalars(stmt).all()

    def create(self, name: str) -> Brand:
        obj = Brand(name=name)
        self.db.add(obj)
        self.db.flush()
        return obj

    def update(self, brand: Brand) -> Brand:
        self.db.flush()
        return brand