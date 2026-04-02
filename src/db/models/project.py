import typing

from sqlalchemy import String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from src.db.models.base import Base


if typing.TYPE_CHECKING:
    from src.db.models.place import Place

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)

    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    places: Mapped[List["Place"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )