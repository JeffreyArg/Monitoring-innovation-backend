from pydantic import BaseModel, Field

class CreateBrandDto(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class UpdateBrandDto(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    was_deleted: bool | None = None

class GetBrandDto(BaseModel):
    id: int
    name: str
    was_deleted: bool
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        from_attributes = True
