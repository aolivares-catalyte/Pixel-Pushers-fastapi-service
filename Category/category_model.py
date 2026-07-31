"""SQLAlchemy model for product categories."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from Product.product_model import Product


# pylint: disable=too-few-public-methods
class Category(Base):
    """Persisted category that groups related products."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="No description provided.",
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
