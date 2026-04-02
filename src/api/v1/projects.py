from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.schemas.pagination import PaginatedResponse
from src.schemas.project import (
    ProjectCreate,
    ProjectListItem,
    ProjectResponse,
    ProjectUpdate,
)
from src.services.project_service import ProjectService
from src.system.resources import IoCContainer

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", status_code=201, response_model=ProjectResponse)
@inject
def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(Provide[IoCContainer.project_service]),
):
    project = service.create_project(data)
    return project


@router.get("", response_model=PaginatedResponse[ProjectListItem])
@inject
def list_projects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    service: ProjectService = Depends(Provide[IoCContainer.project_service]),
):
    projects, total = service.list_projects(page=page, per_page=per_page)
    return PaginatedResponse.create(
        items=projects, total=total, page=page, per_page=per_page
    )


@router.get("/{project_id}", response_model=ProjectResponse)
@inject
def get_project(
    project_id: int,
    service: ProjectService = Depends(Provide[IoCContainer.project_service]),
):
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=ProjectResponse)
@inject
def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(Provide[IoCContainer.project_service]),
):
    return service.update_project(project_id, data)


@router.delete("/{project_id}", status_code=204)
@inject
def delete_project(
    project_id: int,
    service: ProjectService = Depends(Provide[IoCContainer.project_service]),
):
    service.delete_project(project_id)
