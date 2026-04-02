from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.db.models.base import Base


def build_session_factory(db_uri: str) -> sessionmaker[Session]:
    engine = create_engine(db_uri, echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)
