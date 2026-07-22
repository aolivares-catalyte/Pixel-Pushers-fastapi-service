from fastapi import APIRouter, status

from Product.product_schema import ProductSchema

router = APIRouter()

products_list = []

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductSchema):
    """Create a new product with the provided details."""
    products_list.append(product)
    return {"data": product.model_dump()}