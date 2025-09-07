from datetime import datetime
from pydantic import BaseModel, Field

from app.dtos.brand import GetBrandDto
from app.dtos.locality import GetLocalityDto

class CreateVehicleDto(BaseModel):
    brand_id: int
    locality_id: int
    applicant_name: str = Field(..., min_length=2, max_length=120)

class UpdateVehicleDto(BaseModel):
    brand_id: int | None = None
    locality_id: int | None = None
    applicant_name: str | None = Field(None, min_length=2, max_length=120)
    was_deleted: bool | None = None

class GetVehicleDto(BaseModel):
    id: int
    brand_id: int
    locality_id: int
    applicant_name: str
    was_deleted: bool
    brand: GetBrandDto | None = None
    locality: GetLocalityDto | None = None

    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        from_attributes = True
