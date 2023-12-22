"""Database module."""

from sqlalchemy.exc import OperationalError
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def recreate_database(self) -> None:
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)


    def database_exists(self) -> bool:
        try:
            # Attempt to create a temporary connection to check if the database exists
            conn = self._engine.connect()
            conn.close()
            return True
        except OperationalError:
            return False

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            # logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
