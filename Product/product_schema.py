from pydantic import BaseModel, Field, field_validator

class ProductSchema(BaseModel):
    """
    Schema representing a product in inventory.

    Fields:
        name (str): Name of the product.
        unit (str): Unit of measurement for the product (e.g., "each", "lb").
        cost_per_unit (float): Cost of the product per unit. Must be greater than 0.
        price_per_unit (float): Selling price of the product per unit.
        quantity_in_stock (float): Quantity of the product currently in stock.
                                   Must be greater than or equal to 0.
    """
    name: str
    unit: str
    cost_per_unit: float = Field(..., gt=0)
    price_per_unit: float
    quantity_in_stock: float = Field(..., ge=0)