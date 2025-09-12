from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.vehicles import VehicleService
from app.dtos.vehicle import CreateVehicleDto, UpdateVehicleDto, GetVehicleDto

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/", response_model=list[GetVehicleDto])
def list_vehicles(
    brand_id: int | None = Query(None),
    locality_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    return VehicleService(db).list(brand_id=brand_id, locality_id=locality_id)

@router.post("/", response_model=GetVehicleDto, status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: CreateVehicleDto, db: Session = Depends(get_db)):
    return VehicleService(db).create(payload)

@router.get("/{vehicle_id}", response_model=GetVehicleDto)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return VehicleService(db).get(vehicle_id)

@router.patch("/{vehicle_id}", response_model=GetVehicleDto)
def update_vehicle(vehicle_id: int, payload: UpdateVehicleDto, db: Session = Depends(get_db)):
    return VehicleService(db).update(vehicle_id, payload)

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    VehicleService(db).delete(vehicle_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

