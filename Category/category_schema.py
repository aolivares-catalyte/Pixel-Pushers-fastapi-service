"""Pydantic schemas used by the category API routes."""

from pydantic import BaseModel, ConfigDict, Field

from Product.product_schema import ProductRead


class CategoryCreate(BaseModel):
    """Payload schema for creating or replacing a category."""

    name: str
    description: str = Field(default="No description provided.")


class CategoryRead(BaseModel):
    """Response schema for a single category."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class CategoryListResponse(BaseModel):
    """Response envelope for category collection endpoints."""

    message: str
    categories: list[CategoryRead]


class CategoryReadWithProducts(BaseModel):
    """Response schema for a category including nested products."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    products: list[ProductRead] = Field(default_factory=list)
