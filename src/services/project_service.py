from loguru import logger
from sqlalchemy.orm import Session, sessionmaker

from src.clients.artic_client import ArticClient
from src.core.exceptions import BusinessLogicError, NotFoundError
from src.db.models.place import Place
from src.db.models.project import Project
from src.db.repositories.place_repository import PlaceRepository
from src.db.repositories.project_repository import ProjectRepository
from src.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        project_repo: ProjectRepository,
        place_repo: PlaceRepository,
        artic_client: ArticClient,
    ):
        self.session_factory = session_factory
        self.project_repo = project_repo
        self.place_repo = place_repo
        self.artic_client = artic_client

    def create_project(self, data: ProjectCreate) -> Project:
        logger.info(
            f"Creating project '{data.name}' "
            f"with {len(data.place_external_ids)} places"
        )

        artworks = {}
        for ext_id in data.place_external_ids:
            logger.info(
                f"Validating artwork external_id={ext_id} "
                f"via Art Institute API"
            )
            artwork = self.artic_client.get_artwork(ext_id)
            artworks[ext_id] = artwork

        with self.session_factory() as session:
            project = Project(
                name=data.name,
                description=data.description,
                start_date=data.start_date,
            )
            self.project_repo.create(session, project)
            logger.info(f"Project created with id={project.id}")

            for ext_id in data.place_external_ids:
                artwork = artworks[ext_id]
                place = Place(
                    project_id=project.id,
                    external_id=ext_id,
                    title=artwork.title,
                )
                self.place_repo.create(session, place)
                logger.info(
                    f"Place external_id={ext_id} "
                    f"added to project_id={project.id}"
                )

            project = self.project_repo.get_by_id(session, project.id)
            return project

    def get_project(self, project_id: int) -> Project:
        logger.info(f"Fetching project_id={project_id}")
        with self.session_factory() as session:
            project = self.project_repo.get_by_id(session, project_id)
            if not project:
                logger.warning(f"Project with id={project_id} not found")
                raise NotFoundError("Project", project_id)
            return project

    def list_projects(
        self, page: int = 1, per_page: int = 20
    ) -> tuple[list[Project], int]:
        logger.info(f"Listing projects page={page} per_page={per_page}")
        with self.session_factory() as session:
            offset = (page - 1) * per_page
            projects = self.project_repo.get_all(
                session, offset=offset, limit=per_page
            )
            total = self.project_repo.count(session)
            logger.info(
                f"Listed {len(projects)} projects out of {total} total"
            )
            return projects, total

    def update_project(self, project_id: int, data: ProjectUpdate) -> Project:
        logger.info(f"Updating project_id={project_id}")
        with self.session_factory() as session:
            project = self.project_repo.get_by_id(session, project_id)
            if not project:
                logger.warning(f"Project with id={project_id} not found")
                raise NotFoundError("Project", project_id)

            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                logger.info(f"No fields to update for project_id={project_id}")
                return project

            self.project_repo.update(session, project, update_data)
            logger.info(
                f"Project id={project_id} "
                f"updated fields: {list(update_data.keys())}"
            )
            return project

    def delete_project(self, project_id: int) -> None:
        logger.info(f"Deleting project_id={project_id}")
        with self.session_factory() as session:
            project = self.project_repo.get_by_id(session, project_id)
            if not project:
                logger.warning(f"Project with id={project_id} not found")
                raise NotFoundError("Project", project_id)

            has_visited = any(p.visited for p in project.places)
            if has_visited:
                logger.warning(
                    f"Cannot delete project_id={project_id}: "
                    f"has visited places"
                )
                raise BusinessLogicError(
                    "Cannot delete project with visited places"
                )

            self.project_repo.delete(session, project)
            logger.info(f"Project id={project_id} deleted")
