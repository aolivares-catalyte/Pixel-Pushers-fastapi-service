from fastapi import APIRouter, status

from Product.product_schema import ProductSchema

# Create a router instance for product related endpoints
router = APIRouter()

# In memory list to store products
products_list = []


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductSchema):
    """
    Create a new product with the provided details.

    FastAPI automatically validates the incoming request body
    against ProductSchema. If validation fails (e.g., negative
    cost_per_unit or quantity_in_stock), FastAPI will return a 422
    response before this function is executed.
    """
    products_list.append(product)
    return {"data": product.model_dump()}


@router.get("/", status_code=status.HTTP_200_OK)
def get_products():
    """
    Retrieve all products currently stored in memory.
    """
    return {"data": products_list}


@router.get("/search", status_code=status.HTTP_200_OK)
def search_product(name: str, unit: str = "each"):
    """
    Search for a product by name and unit.

    Query parameters:
        name: The product name to search for.
        unit: Optional unit filter (defaults to "each").
    """
    return {
        "data": [
            product
            for product in products_list
            if product.name == name and product.unit == unit
        ]
    }
