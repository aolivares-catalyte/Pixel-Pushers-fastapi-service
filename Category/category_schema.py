from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    """Schema for creating a new category."""

    name: str


class CategoryRead(BaseModel):
    """Schema for reading a category."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductReadBase(BaseModel):
    """
    Base schema for a product returned INSIDE a category.
    It deliberately omits the category_id and category object to prevent infinite loops.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    unit: str
    cost_per_unit: float = Field(gt=0)
    price_per_unit: float
    quantity_in_stock: float = Field(ge=0)

    @field_validator("price_per_unit")
    def validate_price_not_loss(cls, value, info):
        cost = info.data.get("cost_per_unit")
        if cost is not None and value < cost:
            raise ValueError(
                "price_per_unit must be greater than or equal to cost_per_unit"
            )
        return value


class CategoryWithProducts(CategoryRead):
    """
    Nested schema for retrieving a category along with all its associated products.
    """

    products: list[ProductReadBase]
