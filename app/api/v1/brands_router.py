from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.brands import BrandService
from app.dtos.brand import CreateBrandDto, UpdateBrandDto, GetBrandDto

router = APIRouter(prefix="/brands", tags=["brands"])

@router.get("/", response_model=list[GetBrandDto])
def list_brands(db: Session = Depends(get_db)):
    return BrandService(db).list()

@router.post("/", response_model=GetBrandDto, status_code=201)
def create_brand(payload: CreateBrandDto, db: Session = Depends(get_db)):
    return BrandService(db).create(payload)

@router.get("/{brand_id}", response_model=GetBrandDto)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    return BrandService(db).get(brand_id)

@router.patch("/{brand_id}", response_model=GetBrandDto)
def update_brand(brand_id: int, payload: UpdateBrandDto, db: Session = Depends(get_db)):
    return BrandService(db).update(brand_id, payload)
