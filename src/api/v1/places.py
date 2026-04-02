from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.schemas.pagination import PaginatedResponse
from src.schemas.place import PlaceCreate, PlaceResponse, PlaceUpdate
from src.services.place_service import PlaceService
from src.system.resources import IoCContainer

router = APIRouter(prefix="/projects/{project_id}/places", tags=["places"])


@router.post("", status_code=201, response_model=PlaceResponse)
@inject
def add_place(
    project_id: int,
    data: PlaceCreate,
    service: PlaceService = Depends(Provide[IoCContainer.place_service]),
):
    return service.add_place(project_id, data)


@router.get("", response_model=PaginatedResponse[PlaceResponse])
@inject
def list_places(
    project_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    service: PlaceService = Depends(Provide[IoCContainer.place_service]),
):
    places, total = service.list_places(
        project_id, page=page, per_page=per_page
    )
    return PaginatedResponse.create(
        items=places, total=total, page=page, per_page=per_page
    )


@router.get("/{place_id}", response_model=PlaceResponse)
@inject
def get_place(
    project_id: int,
    place_id: int,
    service: PlaceService = Depends(Provide[IoCContainer.place_service]),
):
    return service.get_place(project_id, place_id)


@router.patch("/{place_id}", response_model=PlaceResponse)
@inject
def update_place(
    project_id: int,
    place_id: int,
    data: PlaceUpdate,
    service: PlaceService = Depends(Provide[IoCContainer.place_service]),
):
    return service.update_place(project_id, place_id, data)
