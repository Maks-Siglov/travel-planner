from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from src.db.models.project import Project


class ProjectRepository:
    def get_by_id(self, session: Session, project_id: int) -> Project | None:
        stmt = (
            select(Project)
            .options(joinedload(Project.places))
            .where(Project.id == project_id)
        )
        return session.execute(stmt).unique().scalar_one_or_none()

    def get_all(
        self, session: Session, offset: int = 0, limit: int = 20
    ) -> list[Project]:
        stmt = select(Project).offset(offset).limit(limit)
        return list(session.execute(stmt).scalars().all())

    def count(self, session: Session) -> int:
        stmt = select(func.count(Project.id))
        return session.execute(stmt).scalar_one()

    def create(self, session: Session, project: Project) -> Project:
        session.add(project)
        session.commit()
        return project

    def update(
        self, session: Session, project: Project, data: dict
    ) -> Project:
        for key, value in data.items():
            setattr(project, key, value)
        session.commit()
        return project

    def delete(self, session: Session, project: Project) -> None:
        session.delete(project)
        session.commit()
