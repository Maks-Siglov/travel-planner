from dependency_injector import containers, providers

from src.clients.artic_client import ArticClient
from src.config import Settings, settings
from src.db.repositories.place_repository import PlaceRepository
from src.db.repositories.project_repository import ProjectRepository
from src.db.session import build_session_factory
from src.services.place_service import PlaceService
from src.services.project_service import ProjectService


class IoCContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.api"])

    config: Settings = providers.Configuration()

    # ========================= DB =========================

    session_factory = providers.Singleton(
        build_session_factory,
        db_uri=settings.db_uri,
    )

    # ===================== REPOSITORIES ====================

    project_repo = providers.Singleton(ProjectRepository)
    place_repo = providers.Singleton(PlaceRepository)

    # ======================== CLIENTS =====================

    artic_client = providers.Singleton(
        ArticClient,
        base_url=settings.ARTIC_BASE_URL,
    )

    # ======================== SERVICES ====================

    project_service = providers.Singleton(
        ProjectService,
        session_factory=session_factory,
        project_repo=project_repo,
        place_repo=place_repo,
        artic_client=artic_client,
    )

    place_service = providers.Singleton(
        PlaceService,
        session_factory=session_factory,
        project_repo=project_repo,
        place_repo=place_repo,
        artic_client=artic_client,
    )
