from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from Product.product_model import Product
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Product.product_model import Product

class Category(Base):
    """
    Defines the Category model for organizing inventory items.

    This module contains the SQLAlchemy ORM mapping for the 'categories' table.
    Each Category instance stores a unique name and maintains a relationship
    with associated Product instances.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False, default="No description provided.")

    products: Mapped[list[Product]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )