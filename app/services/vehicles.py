from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.vehicle import VehicleRepository
from app.repository.brand import BrandRepository
from app.repository.locality import LocalityRepository
from app.dtos.vehicle import CreateVehicleDto, UpdateVehicleDto

class VehicleService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = VehicleRepository(db)
        self.brand_repo = BrandRepository(db)
        self.locality_repo = LocalityRepository(db)

    def list(self, *, brand_id: int | None = None, locality_id: int | None = None):
        return self.repo.list(brand_id=brand_id, locality_id=locality_id)

    def get(self, vehicle_id: int):
        v = self.repo.get(vehicle_id)
        if not v:
            raise HTTPException(404, "Vehicle not found")
        return v

    def create(self, payload: CreateVehicleDto):
        brand = self.brand_repo.get(int(payload.brand_id))
        if not brand or brand.was_deleted:
            raise HTTPException(400, "Invalid brand_id")

        locality = self.locality_repo.get(int(payload.locality_id))
        if not locality or locality.was_deleted:
            raise HTTPException(400, "Invalid locality_id")

        obj = self.repo.create(
            brand_id=brand.id,
            locality_id=locality.id,
            applicant_name=payload.applicant_name,
        )
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, vehicle_id: int, payload: UpdateVehicleDto):
        v = self.repo.get(vehicle_id)
        if not v:
            raise HTTPException(404, "Vehicle not found")

        data = payload.model_dump(exclude_unset=True)

        if "brand_id" in data and data["brand_id"] is not None:
            brand = self.brand_repo.get(int(data["brand_id"]))
            if not brand or brand.was_deleted:
                raise HTTPException(400, "Invalid brand_id")
            v.brand_id = brand.id

        if "locality_id" in data and data["locality_id"] is not None:
            loc = self.locality_repo.get(int(data["locality_id"]))
            if not loc or loc.was_deleted:
                raise HTTPException(400, "Invalid locality_id")
            v.locality_id = loc.id

        if "applicant_name" in data and data["applicant_name"] is not None:
            v.applicant_name = data["applicant_name"]

        if "was_deleted" in data and data["was_deleted"] is not None:
            v.was_deleted = bool(data["was_deleted"])

        self.repo.update(v)
        self.db.commit()
        self.db.refresh(v)
        return v
