# Day 4, 5, and 7 Technical Requirements Spec

## API Contract Summary

### Endpoints That Satisfy the Business Requirements

- POST /products
    - Purpose: Persist a new product.
- POST /categories
    - Purpose: Persist a new category.
- GET /products
    - Purpose: View the full catalog.
- GET /products/{id}
    - Purpose: Look up one specific product by identifier.
- GET /products/search?name={name}&unit={unit}
    - Purpose: Search for products by name and optional unit.
- GET /categories/{id}
    - Purpose: View a category together with all products assigned to it.
- PUT /products/{id}
    - Purpose: Fully update an existing product with full replacement.
- PATCH /products/{id}
    - Purpose: Update only the fields provided in the request body.
- DELETE /products/{id}
    - Purpose: Soft delete a product (mark as deleted; not permanently removed).
- DELETE /categories/{id}
    - Purpose: Delete a category only when it has no products assigned to it.

### Request Body Shape

- **POST /products** request body (**ProductCreate**):
    - **All fields required.**
    ```json
    {
        "name": "Basil Plant",
        "unit": "each",
        "cost_per_unit": 1.25,
        "price_per_unit": 2.5,
        "quantity_in_stock": 40,
        "category_id": 2
    }
    ```
- **POST /categories** request body (**CategoryCreate**):
    - **All fields required.**
    ```json
    {
        "name": "Tools"
    }
    ```
- **PUT /products/{id}** request body (**ProductFullUpdate**):
    - **Full replacement. All fields required.**
    ```json
    {
        "name": "Basil Plant",
        "unit": "each",
        "cost_per_unit": 1.25,
        "price_per_unit": 2.5,
        "quantity_in_stock": 40
    }
    ```
- **PATCH /products/{id}** request body (**ProductUpdatePartial**):
    - **Only provided fields are updated. All fields optional.**
    ```json
    {
        "name": "Large Basil Plant",
        "quantity_in_stock": 55
    }
    ```
- **GET /products**, **GET /products/{id}**, and **GET /products/search** do not use a request body.

### Input Validation Rules

Validation occurs at the **Pydantic layer**:

```
cost_per_unit > 0
price_per_unit >= cost_per_unit
quantity_in_stock >= 0
```

- **PUT**: all fields validated
- **PATCH**: only provided fields validated
- **Invalid input** returns **422 Unprocessable Entity**

### Relationship Model and Constraints

- A category is the parent resource and contains an `id` and `name`.
- A product is the child resource and contains a `category_id` foreign key that points to Category.id.
- The foreign key is owned by Product because the child row stores the parent reference.
- A product cannot exist without a valid `category_id`; it must always be attached to a real category.
- `GET /categories/{id}` returns a category response that includes a nested `products` array.
- A product response includes category information (for example, the category's `id` and `name`) instead of only an opaque internal id.
- Categories cannot be deleted if they still contain products.

### Nested Schema Guidance

- Use `ProductRead` for standalone product responses and include category details in that payload.
- Use `CategoryWithProducts` for `GET /categories/{id}` and include a nested `products` array.
- If needed, a smaller `ProductInCategory` schema can be used for products shown inside a category response, but the API contract must remain explicit.

### Successful Response Shapes

- **POST /products**
    - Status: **201 Created**
    - Body:
    ```json
    {
        "id": 101,
        "name": "Basil Plant",
        "unit": "each",
        "cost_per_unit": 1.25,
        "price_per_unit": 2.5,
        "quantity_in_stock": 40,
        "category": {
            "id": 2,
            "name": "Tools"
        }
    }
    ```

- **POST /categories**
    - Status: **201 Created**
    - Body:
    ```json
    {
        "id": 2,
        "name": "Tools"
    }
    ```

- **GET /categories/{id}**
    - Status: **200 OK**
    - Body:
    ```json
    {
        "id": 2,
        "name": "Tools",
        "products": [
            {
                "id": 101,
                "name": "Basil Plant",
                "unit": "each",
                "cost_per_unit": 1.25,
                "price_per_unit": 2.5,
                "quantity_in_stock": 40
            }
        ]
    }
    ```

- **GET /categories/{id}**
    - Status: **200 OK**
    - Body:
    ```json
    {
        "id": 2,
        "name": "Tools",
        "products": [
            {
                "id": 101,
                "name": "Basil Plant",
                "unit": "each",
                "cost_per_unit": 1.25,
                "price_per_unit": 2.5,
                "quantity_in_stock": 40
            }
        ]
    }
    ```

- **GET /products**
    - Status: **200 OK**
    - Returns: **ProductListResponse** containing a **list of ProductRead** objects
    - Body (non-empty):
    ```json
    {
        "message": "Products retrieved successfully",
        "products": [
            {
                "id": 101,
                "name": "Basil Plant",
                "unit": "each",
                "cost_per_unit": 1.25,
                "price_per_unit": 2.5,
                "quantity_in_stock": 40
            }
        ]
    }
    ```
    - Body (empty list):
    ```json
    {
        "message": "No products found",
        "products": []
    }
    ```

- **GET /products/{id}**
    - Status: **200 OK**
    - Body:
    ```json
    {
        "id": 101,
        "name": "Basil Plant",
        "unit": "each",
        "cost_per_unit": 1.25,
        "price_per_unit": 2.5,
        "quantity_in_stock": 40,
        "category": {
            "id": 2,
            "name": "Tools"
        }
    }
    ```

- **GET /products/search?name={name}&unit={unit}**
    - Status: **200 OK**
    - Body (matches found):
    ```json
    {
        "message": "Matching products found",
        "results": [
            {
                "id": 101,
                "name": "Basil Plant",
                "unit": "each",
                "cost_per_unit": 1.25,
                "price_per_unit": 2.5,
                "quantity_in_stock": 40
            }
        ]
    }
    ```
    - Body (no matches):
    ```json
    {
        "message": "No matching products found",
        "results": []
    }
    ```

- **PUT /products/{id}**
    - Status: **200 OK**
    - Body: **ProductRead**
    ```json
    {
        "id": 101,
        "name": "Basil Plant",
        "unit": "each",
        "cost_per_unit": 1.25,
        "price_per_unit": 2.50,
        "quantity_in_stock": 40
    }
    ```

- **DELETE /products/{id}**
    - Status: **204 No Content**
    - Body: None

- **DELETE /categories/{id}**
    - Status: **204 No Content**
    - Body: None

- **PATCH /products/{id}**
    - Status: **200 OK**
    - Body: **ProductRead**
    ```json
    {
        "id": 101,
        "name": "Large Basil Plant",
        "unit": "each",
        "cost_per_unit": 1.25,
        "price_per_unit": 2.5,
        "quantity_in_stock": 55
    }
    ```

### Failure Responses

- **Endpoint**: **GET, PUT, DELETE, PATCH /products/{id}**
- When product does not exist **or is soft-deleted**:
    - Status: **404 Not Found**
    - Body:
    ```json
    {
        "detail": "Product not found"
    }
    ```
    - Note: Soft-deleted products behave as if they don't exist; clients cannot distinguish between a hard-deleted and soft-deleted product

- **Endpoint**: **PUT, PATCH /products/{id}**
- When product body is invalid:
    - Status: **422 Unprocessable Entity**
    - Body: Pydantic validation error

- **Endpoint**: **POST /products**
- When product body is invalid:
    - Status: **422 Unprocessable Entity**
    - Body: Pydantic validation error
- When the product references a category that does not exist:
    - Status: **404 Not Found**
    - Body:
    ```json
    {
        "detail": "Category not found"
    }
    ```

- **Endpoint**: **DELETE /categories/{id}**
- When the category still has products assigned to it:
    - Status: **409 Conflict**
    - Body:
    ```json
    {
        "detail": "Cannot delete category with existing products"
    }
    ```

- **Endpoint**: **POST, PUT, PATCH, DELETE /products**, **GET /products**, **GET /products/{id}**, **GET /products/search**
- When a database operation fails (commit, query, etc.):
    - Status: **500 Internal Server Error**
    - Body:
    ```json
    {
        "detail": "Failed to [create/update/delete/retrieve] product in the database."
    }
    ```
    - Error handling: Exception caught, transaction rolled back, error message returned

### Responsibility Split: Validation vs Database vs Route Logic

**Pydantic schema (ProductCreate, ProductFullUpdate, ProductUpdatePartial)**

- Validates incoming request data and constraints before any route logic runs.
- Enforces validation rules:
    ```
    cost_per_unit > 0
    price_per_unit >= cost_per_unit
    quantity_in_stock >= 0
    ```
- **PUT**: all fields validated.
- **PATCH**: only provided fields validated.
- Invalid input is rejected with **422** before route logic proceeds.

**SQLAlchemy model (Product and Category)**

- Maps Python objects to the products and categories tables.
- Represents persisted database records.
- The Product model includes a `category_id` foreign key to Category.id and a `category` relationship.
- The Category model includes a `products` relationship back to Product.
- Does not enforce business validation rules — those belong to **Pydantic**.
- Raises database-level errors only for structural issues (e.g., missing row, constraint violations).

**Route functions + dependency (get_db)**

- Receive already-validated request data.
- **All database operations (commit, query, refresh) are wrapped in try-except blocks**.
- **Query filtering**: All queries automatically filter out soft-deleted products (`WHERE is_deleted = False`):
    - GET /products → returns only active products
    - GET /products/{id} → returns 404 if product is soft-deleted
    - GET /products/search → search results exclude soft-deleted products
- **DELETE /products/{id}**: Updates the product by setting `is_deleted = True` instead of removing the row
- **Error handling pattern**:
    ```
    try:
        db.commit()
        db.refresh(new_product)  // or other query/operation
        return response
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to [operation] product in the database.")
    ```
- Perform lookup/update/delete operations using **SQLAlchemy**.
- Owns not-found logic for **GET/PUT/PATCH/DELETE**:
    - Missing product or soft-deleted product → **404 Not Found**
    - Missing category for product creation → **404 Not Found**
    - Deleting a category that still has products → **409 Conflict**
- **PUT**: replace all fields.
- **PATCH**: update only provided fields.
- **DELETE**: set `is_deleted = True`; return **204** on success.
- Handle commit/refresh on writes and return response payloads.

### Soft Delete Implementation

**Soft Delete Field**:
- **Field name**: `is_deleted` (boolean)
- **Default value**: `False` (product is active)
- **Set to `True`** when **DELETE /products/{id}** is called
- **Never returned** in any Pydantic schema (**ProductRead**, **ProductCreate**, etc.)
- All queries (GET, GET by ID, search) automatically filter out soft-deleted products (`is_deleted = False`)

**Behavior**:
- Deleted products remain in the database but are hidden from all responses
- A soft-deleted product returns **404 Not Found** just like a non-existent product
- This preserves data integrity and allows for recovery if needed

### Returned Fields Decision and Rationale

- **ProductRead** fields returned:
    - `id`
    - `name`
    - `unit`
    - `cost_per_unit`
    - `price_per_unit`
    - `quantity_in_stock`
- **NOT returned** (hidden from API):
    - `is_deleted` (internal implementation detail)
- Why these fields:
    - They are the business fields needed by clients for catalog display, stock checks, and margin awareness.
    - `id` is required for stable single-item lookup and client-side linking.
    - Returning only schema-defined fields prevents ORM/session internals from leaking and keeps the API contract predictable.
    - The `is_deleted` field is an internal implementation detail; clients never see it.

## Technical Specs

### 1. Store Product Objects in Postgres

Given a validated **SQLAlchemy Product** instance, when the application is connected to the Postgres database through the `get_db` session dependency, the instance must be added to the session, committed, and refreshed. The resulting record must be permanently stored in the products table and returned to the client using **ProductRead**.

- The persistence operation occurs inside the **POST /products** endpoint.
- The endpoint converts a validated Pydantic **ProductCreate** into a **SQLAlchemy Product**.
- The database write flow: open session → add → **try** { commit → refresh } → **catch** rollback → return.
- **Error handling**:
    - Database operation failures are caught in a **try-except** block.
    - On exception: **rollback** the transaction and return **500 Internal Server Error**.
    - Validation errors return **422** (before route logic runs).
    - Database failures return **500** with message: `"Failed to create product in the database."`
- Response:
    - **201 Created** with **ProductRead** (on success).
    - No SQLAlchemy objects are returned directly.

### 2. List All Products

When a client performs a **GET /products** request, the service queries the Postgres products table using the **SQLAlchemy** session provided by `get_db`. The endpoint returns **200 OK** with a **ProductListResponse** containing a **list of ProductRead** objects.

- **Endpoint**: **GET /products**
- **Returns**: **List of ProductRead** objects wrapped in **ProductListResponse**
- **Database interaction**:
    - Use `db.query(Product).all()`.
    - No filtering and no pagination for Day 4.
- **Response shape**:
    - **200 OK** with **ProductListResponse**
        - Body (non-empty):
        ```json
        {
            "message": "Products retrieved successfully",
            "products": [
                {
                    "id": 101,
                    "name": "Basil Plant",
                    "unit": "each",
                    "cost_per_unit": 1.25,
                    "price_per_unit": 2.5,
                    "quantity_in_stock": 40
                }
            ]
        }
        ```
        - Body (empty):
        ```json
        {
            "message": "No products found",
            "products": []
        }
        ```
- **Empty catalog behavior**:
    - Return **200 OK**.
    - Return `products` as an empty list.
    - Return `message` as `"No products found"`.
    - Soft-deleted products are automatically excluded (not counted as products).

### 3. Get Product by ID

When a client performs a **GET /products/{id}** request, the service queries the products table by primary key. If the product exists, return **200 OK** with a single **ProductRead** object. If the product does not exist, return **404 Not Found** with a clear message.

- **Endpoint**: **GET /products/{id}**
- **Path parameters**:
    - `id`: `int`
- **Response behavior**:
    - **Found**: **200 OK** with **ProductRead**.
    - **Not found**: **404 Not Found** with message `"Product not found"`.

### 4. Search Products by Name and Optional Unit

When a client performs a **GET /products/search** request with query parameters, the service returns matching products from Postgres. Search responses always use **list semantics** and never return **404** for no matches.

- **Endpoint**: **GET /products/search?name={name}&unit={unit}**
- **Query parameters**:
    - `name`: `str` (required)
    - `unit`: `Optional[str]` (default: `"each"`)
- **Search logic**:
    ```python
    query = db.query(Product)
    query = query.filter(Product.name.ilike(f"%{name}%"))
    if unit:
        query = query.filter(Product.unit == unit)
    results = query.all()
    ```
- **Response shape**:
    - **200 OK**
        - Body (matches found):
        ```json
        {
            "message": "Matching products found",
            "results": [
                {
                    "id": 101,
                    "name": "Basil Plant",
                    "unit": "each",
                    "cost_per_unit": 1.25,
                    "price_per_unit": 2.5,
                    "quantity_in_stock": 40
                }
            ]
        }
        ```
        - Body (no matches):
        ```json
        {
            "message": "No matching products found",
            "results": []
        }
        ```
- **Empty search behavior**:
    - Return **200 OK**.
    - Return `results` as an empty list.
    - Return `message` as `"No matching products found"`.
    - Soft-deleted products are automatically excluded from search results.

### 5. Response Model Enforcement

All product and category endpoints must return **Pydantic response models** rather than raw **SQLAlchemy objects**.

- **ProductRead** is the response schema for returning one product object.
- **CategoryRead** is the response schema for returning one category object.
- **CategoryWithProducts** is the response schema for **GET /categories/{id}** and includes a nested `products` array.
- **Endpoint mapping**:
    - **POST /products** → **ProductRead**
    - **POST /categories** → **CategoryRead**
    - **GET /products/{id}** → **ProductRead**
    - **GET /products** → **ProductListResponse** (contains message and list of **ProductRead**)
    - **GET /products/search** → object containing message and list of **ProductRead**
    - **GET /categories/{id}** → **CategoryWithProducts**
- **SQLAlchemy** objects must be serialized through **Pydantic** before returning.

### 6. Database Session Dependency

All product endpoints must use the `get_db` **FastAPI dependency** to obtain a database session. Route handlers must not manually create sessions.

- **Use**: `db: Session = Depends(get_db)`
- **Dependency responsibilities**:
    - Open and close the session.
- **Route responsibilities**:
    - Execute query logic.
    - Commit for successful writes.
    - Roll back when write operations fail.
- **Benefits**:
    - Prevents connection leaks.
    - Keeps transaction handling explicit and consistent.

### 7. Input Validation

All incoming product and category requests must be validated using their respective **Pydantic schemas**. Invalid data must return **422 Unprocessable Entity** from **FastAPI/Pydantic**.

- **Validation by endpoint**:
    - **POST /products**: Validate with **ProductCreate** (all fields required, including a valid `category_id`).
    - **POST /categories**: Validate with **CategoryCreate** (all fields required).
    - **PUT /products/{id}**: Validate with **ProductFullUpdate** (all fields required) - to be defined for Day 5.
    - **PATCH /products/{id}**: Validate with **ProductUpdatePartial** (fields are optional) - to be defined for Day 5.
    - Pydantic enforces field types and constraints.
- **Error behavior**:
    - **FastAPI** automatically returns **422** with validation details.
- **Conversion**:
    - Validated schema is converted to **SQLAlchemy Product** or **SQLAlchemy Category** before persistence.

### 8. Consistent API Shape

All product and category endpoints must follow a **predictable response contract**.

- **Single-resource endpoints** return one object:
    - **POST /products** → **ProductRead**
    - **POST /categories** → **CategoryRead**
    - **GET /products/{id}** → **ProductRead**
    - **GET /categories/{id}** → **CategoryWithProducts**
- **List endpoints** return an object with a message and a list:
    - **GET /products** → **ProductListResponse** (contains message and **list of ProductRead**)
    - **GET /products/search** → `{ message, results: [list of ProductRead] }`
- **Empty list responses** are explicit and informative:
    - `products: []` with message `"No products found"`
    - `results: []` with message `"No matching products found"`
- No null list fields and no mixed object-or-list return types.

### 9. No SQLAlchemy Leakage

The API must never return raw **SQLAlchemy** model instances, session-bound objects, or ORM-specific fields.

- **SQLAlchemy internals** such as `_sa_instance_state` must never appear in response payloads.
- Use **ProductRead** and **CategoryRead** for serialization.
- **Ensures**:
    - Clean JSON
    - Stable API contract
    - No accidental exposure of internal implementation details

## List of Business Requirements

1. Persist New Products

As a garden center manager, I want new products to be permanently saved when they are added to the system, so that the catalog does not disappear every time the server restarts.

2. View the Full Catalog

As a garden center employee, I want to see a list of every product currently in the system, so that I can review what is in stock.

3. Look Up a Single Product

As a garden center employee, I want to look up one specific product by its identifier, so that I can quickly check details without scanning the entire catalog.

4. Search Products and See Clear Empty Results

As a garden center employee, I want a clear message when no products match my catalog or search request, so that I can tell the difference between an empty result and a failure.

5. API Responses Do Not Leak Implementation Details

As the garden center technology partner, I want the data returned by the API to be intentional and controlled, so that the API has a stable and predictable contract regardless of internal database structure.

## List of Business Requirements Day 5

1. Update an Existing Product

As a garden center manager, I want to update a product's details (price, cost, stock, name) after it's been created, so that the catalog reflects reality without needing to delete and recreate the item.

2. Remove a Discontinued Product

As a garden center manager, I want to soft delete a product from the catalog, so that discontinued items no longer show up for staff or customers, but the data is preserved for historical and recovery purposes.

3. Clear Failure When Updating or Deleting Something That Doesn't Exist

As a garden center employee, I want a clear, correct response when I try to update or delete a product that isn't in the system, so that I know immediately it wasn't found rather than getting a server error or a false success.

4. Reject Invalid Data Before It Reaches the Database

As the garden center's technology partner, I want obviously invalid input (like a negative price) rejected immediately with a readable explanation, so that bad data never gets a chance to corrupt the catalog and staff aren't left guessing what went wrong.

5. A Predictable, Documented Contract for Every Outcome

As the garden center's technology partner, I want every endpoint's possible responses, success and failure, documented and verifiable, so that anyone integrating with this API knows exactly what to expect in every case.

