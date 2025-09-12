from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.entities.locality import Locality

class LocalityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, locality_id: int) -> Optional[Locality]:
        return self.db.get(Locality, locality_id)

    def get_by_name(self, name: str) -> Optional[Locality]:
        stmt = select(Locality).where(Locality.name == name)
        return self.db.scalar(stmt)

    def list(self, include_deleted: bool = False) -> Iterable[Locality]:
        stmt = select(Locality)
        if not include_deleted:
            stmt = stmt.where(Locality.was_deleted.is_(False))
        return self.db.scalars(stmt).all()

    def create(self, name: str) -> Locality:
        obj = Locality(name=name)
        self.db.add(obj)
        self.db.flush()
        return obj

    def update(self, locality: Locality) -> Locality:
        self.db.flush()
        return locality
