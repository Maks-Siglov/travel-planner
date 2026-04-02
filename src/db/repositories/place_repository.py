from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.models.place import Place


class PlaceRepository:
    def get_by_id(self, session: Session, place_id: int) -> Place | None:
        return session.get(Place, place_id)

    def get_by_project_and_id(
        self, session: Session, project_id: int, place_id: int
    ) -> Place | None:
        stmt = select(Place).where(
            Place.project_id == project_id, Place.id == place_id
        )
        return session.execute(stmt).scalar_one_or_none()

    def get_all_by_project(
        self,
        session: Session,
        project_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Place]:
        stmt = (
            select(Place)
            .where(Place.project_id == project_id)
            .offset(offset)
            .limit(limit)
        )
        return list(session.execute(stmt).scalars().all())

    def count_by_project(self, session: Session, project_id: int) -> int:
        stmt = select(func.count(Place.id)).where(
            Place.project_id == project_id
        )
        return session.execute(stmt).scalar_one()

    def create(self, session: Session, place: Place) -> Place:
        session.add(place)
        session.commit()
        return place

    def update(self, session: Session, place: Place, data: dict) -> Place:
        for key, value in data.items():
            setattr(place, key, value)
        session.commit()
        return place
