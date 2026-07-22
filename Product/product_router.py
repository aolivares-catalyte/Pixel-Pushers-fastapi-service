from fastapi import APIRouter, status

from Product.product_schema import ProductSchema

router = APIRouter()

products_list = []


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductSchema):
    """Create a new product with the provided details."""
    products_list.append(product)
    return {"data": product.model_dump()}


@router.get("/products", status_code=status.HTTP_200_OK)
def get_products():
    """Get all products."""
    return {"data": products_list}


@router.get("/products/search", status_code=status.HTTP_200_OK)
def search_product(name: str, unit: str = "each"):
    """Search for a product by name and unit."""
    return {
        "data": [
            product
            for product in products_list
            if product.name == name and product.unit == unit
        ]
    }
