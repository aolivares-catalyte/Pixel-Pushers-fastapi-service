from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Product.product_model import Product


class Category(Base):
    """
    Defines the Category model for organizing inventory items.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")
