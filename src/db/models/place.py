import typing

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if typing.TYPE_CHECKING:
    from src.db.models.project import Project


class Place(Base):
    __tablename__ = "places"
    __table_args__ = (UniqueConstraint("project_id", "external_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )

    external_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str | None] = mapped_column(String, nullable=True)

    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    visited: Mapped[bool] = mapped_column(Boolean, default=False)

    project: Mapped["Project"] = relationship(back_populates="places")
