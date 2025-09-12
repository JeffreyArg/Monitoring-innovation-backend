from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository.locality import LocalityRepository
from app.dtos.locality import CreateLocalityDto, UpdateLocalityDto

class LocalityService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = LocalityRepository(db)

    def list(self, include_deleted: bool = False):
        return self.repo.list(include_deleted=include_deleted)

    def get(self, locality_id: int):
        loc = self.repo.get(locality_id)
        if not loc:
            raise HTTPException(404, "Locality not found")
        return loc

    def create(self, payload: CreateLocalityDto):
        if self.repo.get_by_name(payload.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Locality name already exists",
            )
        obj = self.repo.create(name=payload.name)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, locality_id: int, payload: UpdateLocalityDto):
        loc = self.repo.get(locality_id)
        if not loc:
            raise HTTPException(404, "Locality not found")

        data = payload.model_dump(exclude_unset=True)
        if "name" in data and data["name"] is not None:
            exists = self.repo.get_by_name(data["name"])
            if exists and exists.id != loc.id:
                raise HTTPException(409, "Locality name already exists")
            loc.name = data["name"]

        if "was_deleted" in data and data["was_deleted"] is not None:
            loc.was_deleted = bool(data["was_deleted"])

        self.repo.update(loc)
        self.db.commit()
        self.db.refresh(loc)
        return loc
