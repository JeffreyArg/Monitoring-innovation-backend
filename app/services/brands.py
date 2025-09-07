from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository.brand import BrandRepository
from app.dtos.brand import CreateBrandDto, UpdateBrandDto

class BrandService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = BrandRepository(db)

    def list(self, include_deleted: bool = False):
        return self.repo.list(include_deleted=include_deleted)

    def get(self, brand_id: int):
        brand = self.repo.get(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        return brand

    def create(self, payload: CreateBrandDto):
        if self.repo.get_by_name(payload.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Brand name already exists",
            )
        obj = self.repo.create(name=payload.name)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, brand_id: int, payload: UpdateBrandDto):
        brand = self.repo.get(brand_id)
        if not brand:
            raise HTTPException(404, "Brand not found")

        data = payload.model_dump(exclude_unset=True)
        if "name" in data and data["name"] is not None:
            exists = self.repo.get_by_name(data["name"])
            if exists and exists.id != brand.id:
                raise HTTPException(409, "Brand name already exists")
            brand.name = data["name"]

        if "was_deleted" in data and data["was_deleted"] is not None:
            brand.was_deleted = bool(data["was_deleted"])

        self.repo.update(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand
