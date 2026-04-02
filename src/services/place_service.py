from loguru import logger
from sqlalchemy.orm import Session, sessionmaker

from src.clients.artic_client import ArticClient
from src.core.exceptions import BusinessLogicError, NotFoundError
from src.db.models.place import Place
from src.db.repositories.place_repository import PlaceRepository
from src.db.repositories.project_repository import ProjectRepository
from src.schemas.place import PlaceCreate, PlaceUpdate


class PlaceService:
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

    def add_place(self, project_id: int, data: PlaceCreate) -> Place:
        logger.info(
            f"Adding place external_id={data.external_id} "
            f"to project_id={project_id}"
        )

        logger.info(
            f"Validating artwork external_id={data.external_id} "
            f"via Art Institute API"
        )
        artwork = self.artic_client.get_artwork(data.external_id)

        with self.session_factory() as session:
            project = self.project_repo.get_by_id(session, project_id)
            if not project:
                logger.warning(f"Project with id={project_id} not found")
                raise NotFoundError("Project", project_id)

            current_count = self.place_repo.count_by_project(
                session, project_id
            )
            if current_count >= 10:
                logger.warning(
                    f"Project id={project_id} already has "
                    f"{current_count} places (max 10)"
                )
                raise BusinessLogicError(
                    "Project cannot have more than 10 places"
                )

            for existing_place in project.places:
                if existing_place.external_id == data.external_id:
                    logger.warning(
                        f"Place external_id={data.external_id} "
                        f"already exists in project_id={project_id}"
                    )
                    raise BusinessLogicError(
                        f"Place with external_id {data.external_id} "
                        f"already exists in this project"
                    )

            place = Place(
                project_id=project_id,
                external_id=data.external_id,
                title=artwork.get("title"),
            )
            self.place_repo.create(session, place)
            logger.info(
                f"Place id={place.id} (external_id={data.external_id}) "
                f"added to project_id={project_id}"
            )
            return place

    def get_place(self, project_id: int, place_id: int) -> Place:
        logger.info(
            f"Fetching place_id={place_id} from project_id={project_id}"
        )
        with self.session_factory() as session:
            place = self.place_repo.get_by_project_and_id(
                session, project_id, place_id
            )
            if not place:
                logger.warning(
                    f"Place id={place_id} not found in project_id={project_id}"
                )
                raise NotFoundError("Place", place_id)
            return place

    def list_places(
        self, project_id: int, page: int = 1, per_page: int = 20
    ) -> tuple[list[Place], int]:
        logger.info(
            f"Listing places for project_id={project_id} "
            f"page={page} per_page={per_page}"
        )
        with self.session_factory() as session:
            project = self.project_repo.get_by_id(session, project_id)
            if not project:
                logger.warning(f"Project with id={project_id} not found")
                raise NotFoundError("Project", project_id)

            offset = (page - 1) * per_page
            places = self.place_repo.get_all_by_project(
                session, project_id, offset=offset, limit=per_page
            )
            total = self.place_repo.count_by_project(session, project_id)
            logger.info(
                f"Listed {len(places)} places out of {total} total "
                f"for project_id={project_id}"
            )
            return places, total

    def update_place(
        self, project_id: int, place_id: int, data: PlaceUpdate
    ) -> Place:
        logger.info(f"Updating place_id={place_id} in project_id={project_id}")
        with self.session_factory() as session:
            place = self.place_repo.get_by_project_and_id(
                session, project_id, place_id
            )
            if not place:
                logger.warning(
                    f"Place id={place_id} not found in project_id={project_id}"
                )
                raise NotFoundError("Place", place_id)

            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                logger.info(f"No fields to update for place_id={place_id}")
                return place

            self.place_repo.update(session, place, update_data)
            logger.info(
                f"Place id={place_id} "
                f"updated fields: {list(update_data.keys())}"
            )

            if update_data.get("visited") is True:
                self._check_project_completion(session, project_id)

            return place

    def _check_project_completion(
        self, session: Session, project_id: int
    ) -> None:
        project = self.project_repo.get_by_id(session, project_id)
        if project and all(p.visited for p in project.places):
            self.project_repo.update(session, project, {"is_completed": True})
            logger.info(
                f"All places visited — "
                f"project id={project_id} marked as completed"
            )
