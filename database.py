"""
Database configuration module.

This file initializes the SQLAlchemy engine, session factory, and declarative
base class used throughout the application. It also loads environment variable
and applies the create/drop strategy to synchronize the database schema with
the ORM models.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load environment variables from .env file
load_dotenv()

# Retrieve database URL and validate it
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, echo=True)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """Base class for all ORM models."""
