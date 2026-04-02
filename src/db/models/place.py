import typing

from sqlalchemy import ForeignKey, String, Boolean, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from src.db.models.base import Base

if typing.TYPE_CHECKING:
    from src.db.models.project import Project

class Place(Base):
    __tablename__ = "places"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    external_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    visited: Mapped[bool] = mapped_column(Boolean, default=False)

    project: Mapped["Project"] = relationship(
        back_populates="places"
    )