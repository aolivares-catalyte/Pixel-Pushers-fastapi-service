from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    """
    Schema representing a product in inventory.

    Fields:
        name (str): Name of the product.
        unit (str): Unit of measurement for the product (e.g., "each", "lb").
        cost_per_unit (float): Cost of the product per unit. Must be greater than 0.
        price_per_unit (float): Selling price of the product per unit.
                                Must be greater than or equal to cost_per_unit.
        quantity_in_stock (float): Quantity of the product currently in stock.
                                   Must be greater than or equal to 0.
    """

    name: str
    unit: str
    cost_per_unit: float = Field(..., gt=0)
    price_per_unit: float
    quantity_in_stock: float = Field(..., ge=0)

    @field_validator("price_per_unit", mode="before")
    def validate_price_per_unit(cls, value, info):
        """Validate that the product is not being sold at a loss."""
        cost_per_unit = info.data.get("cost_per_unit")
        if cost_per_unit is not None and cost_per_unit > value:
            raise ValueError(
                "price_per_unit must be greater than or equal to cost_per_unit"
            )
        return value


class ProductFullUpdate(BaseModel):
    """
    Schema for fully replacing an existing product (PUT).
    All fields are required.
    """

    name: str
    unit: str
    cost_per_unit: float = Field(..., gt=0)
    price_per_unit: float
    quantity_in_stock: float = Field(..., ge=0)

    @field_validator("price_per_unit", mode="before")
    def validate_price_per_unit(cls, value, info):
        """Validate that the product is not being sold at a loss."""
        cost_per_unit = info.data.get("cost_per_unit")
        if cost_per_unit is not None and cost_per_unit > value:
            raise ValueError(
                "price_per_unit must be greater than or equal to cost_per_unit"
            )
        return value

class ProductUpdatePartial(BaseModel):
    """
    Schema representing a partial update to a product in inventory.

    Fields:
        name (Optional[str]): Name of the product.
        unit (Optional[str]): Unit of measurement for the product (e.g., "each", "lb").
        cost_per_unit (Optional[float]): Cost of the product per unit. Must be greater than 0.
        price_per_unit (Optional[float]): Selling price of the product per unit.
                                           Must be greater than or equal to cost_per_unit.
        quantity_in_stock (Optional[float]): Quantity of the product currently in stock.
                                              Must be greater than or equal to 0.
    """
    name: str | None = None
    unit: str | None = None
    cost_per_unit: float | None = Field(default=None, gt=0)
    price_per_unit: float | None = None
    quantity_in_stock: float | None = Field(default=None, ge=0)

    @field_validator("price_per_unit")
    def validate_price_per_unit(cls, value, info):
        """Validate that the product is not being sold at a loss."""
        cost_per_unit = info.data.get("cost_per_unit")
        if cost_per_unit is not None and cost_per_unit > value:
            raise ValueError("price_per_unit must be greater than or equal to cost_per_unit")
        return value


class ProductRead(BaseModel):
    """
    Schema representing what will be returned in response to a request.

    Fields:
        id (int): Unique identifier of the product.
        name (str): Name of the product.
        unit (str): Unit of measurement of each product (e.g., "each", "lb").
        cost_per_unit (float): Cost of the product per unit. Must be greater than 0.
        price_per_unit (float): Selling price of the product per unit.
                                Must be greater than or equal to cost_per_unit.
        quantity_in_stock (float): Quantity of the product currently in stock.
                                    Must be greater than or equal to 0.
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
            raise ValueError("price_per_unit must be greater than or equal to cost_per_unit")
        return value

class ProductListResponse(BaseModel):
    """
    Schema representing a response containing a list of products.
    """

    message: str
    products: list[ProductRead]
