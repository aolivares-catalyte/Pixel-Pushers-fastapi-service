from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    products = relationship("Product", back_populates="category")
