"""Utility helpers shared across API modules."""

from database import session_local


def get_db():
    """
    Get a database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()
