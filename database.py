"""
Database configuration module.

This file initializes the SQLAlchemy engine, session factory, and declarative
base class used throughout the application. It also loads environment variable
and applies the create/drop strategy to synchronize the database schema with
the ORM models.
"""
import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine 

# Load environment variables from .env file
load_dotenv()

# Retrieve database URL and validate it
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

# Import models after Base is defined to avoid circular imports
from Product.product_model import Product

# Drop and recreate all tables to sync schema with ORM models
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

