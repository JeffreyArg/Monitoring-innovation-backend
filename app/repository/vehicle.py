from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.database.entities.vehicle import Vehicle

class VehicleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.get(Vehicle, vehicle_id)

    def list(
        self,
        *,
        brand_id: int | None = None,
        locality_id: int | None = None,
        include_deleted: bool = False,
        with_relations: bool = True,
    ) -> Iterable[Vehicle]:
        stmt = select(Vehicle)
        if with_relations:
            stmt = stmt.options(joinedload(Vehicle.brand), joinedload(Vehicle.locality))
        if not include_deleted:
            stmt = stmt.where(Vehicle.was_deleted.is_(False))
        if brand_id is not None:
            stmt = stmt.where(Vehicle.brand_id == brand_id)
        if locality_id is not None:
            stmt = stmt.where(Vehicle.locality_id == locality_id)
        return self.db.scalars(stmt).all()

    def create(self, *, brand_id: int, locality_id: int, applicant_name: str) -> Vehicle:
        obj = Vehicle(
            brand_id=brand_id,
            locality_id=locality_id,
            applicant_name=applicant_name,
        )
        self.db.add(obj)
        self.db.flush()
        return obj

    def update(self, vehicle: Vehicle) -> Vehicle:
        self.db.flush()
        return vehicle
