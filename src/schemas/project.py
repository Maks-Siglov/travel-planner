from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.place import PlaceResponse


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None
    place_external_ids: list[int] = Field(default_factory=list, max_length=10)


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    start_date: date | None
    is_completed: bool
    places: list[PlaceResponse]


class ProjectListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    start_date: date | None
    is_completed: bool
