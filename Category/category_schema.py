from pydantic import BaseModel, Field

from Product.product_schema import ProductRead

class CategoryCreate(BaseModel):
    """
    Schema representing a category in the inventory system.

    Fields:
        name (str): Name of the category.
        description (str): Description of the category.
    """

    name: str
    description: str = Field(default="No description provided.")

class CategoryRead(BaseModel):
    """
    Schema representing a category for reading purposes.

    Fields:
        id (int): Unique identifier for the category.
        name (str): Name of the category.
        description (str): Description of the category.
    """

    id: int
    name: str
    description: str

class CategoryListResponse(BaseModel):
    """
    Schema representing a response containing a list of categories.

    Fields:
        message (str): A message indicating the result of the request.
        categories (list[CategoryRead]): A list of categories.
    """

    message: str
    categories: list[CategoryRead]

class CategoryReadWithProducts(BaseModel):
    """
    Schema representing a category along with its associated products.

    Fields:
        products (list[ProductRead]): A list of products associated with the category.
    """

    id: int
    name: str
    description: str
    products: list[ProductRead] = []