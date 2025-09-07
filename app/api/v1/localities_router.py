from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.localities import LocalityService
from app.dtos.locality import CreateLocalityDto, UpdateLocalityDto, GetLocalityDto

router = APIRouter(prefix="/localities", tags=["localities"])

@router.get("/", response_model=list[GetLocalityDto])
def list_localities(db: Session = Depends(get_db)):
    return LocalityService(db).list()

@router.post("/", response_model=GetLocalityDto, status_code=201)
def create_locality(payload: CreateLocalityDto, db: Session = Depends(get_db)):
    return LocalityService(db).create(payload)

@router.get("/{locality_id}", response_model=GetLocalityDto)
def get_locality(locality_id: int, db: Session = Depends(get_db)):
    return LocalityService(db).get(locality_id)

@router.patch("/{locality_id}", response_model=GetLocalityDto)
def update_locality(locality_id: int, payload: UpdateLocalityDto, db: Session = Depends(get_db)):
    return LocalityService(db).update(locality_id, payload)
