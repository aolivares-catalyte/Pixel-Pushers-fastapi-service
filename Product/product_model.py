from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Boolean, ForeignKey
from database import Base

if TYPE_CHECKING:
    from Category.category_model import Category


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
    quantity_in_stock: Mapped[float] = mapped_column(Float, nullable=False, index=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    category: Mapped["Category"] = relationship(back_populates="products")
