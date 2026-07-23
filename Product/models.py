from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer

from database import Base

class Product(Base):
    """
    Defines the Product model used for representing inventory items.

    This module contains the SQLAlchemy ORM mapping for the 'products' table.
    Each Product instance stores core information about an item, including
    its name, unit of measurement, cost, price,, and current stock level.
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    unit: Mapped[str] = mapped_column(String, nullable=False, index=True)
    cost_per_unit: Mapped[float] = mapped_column(Float, nullable=False, index=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False, index=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, nullable=False, index=False)
