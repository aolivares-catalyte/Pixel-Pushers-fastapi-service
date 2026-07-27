## Technical Specification: Garden Center API

### 1. Endpoints & Payloads

The endpoints below belong to the product router, which is mounted under the `/products` prefix. All endpoints must replace the current in-memory `products_list` with the `get_db` FastAPI dependency for database session management.

To support responses with database-generated IDs, a new schema `ProductOut` should be created that inherits from `ProductSchema` and adds an `id` field.

#### 1.1 List Available Plants
*   **Method:** `GET`
*   **Path:** `/products/`
*   **Description:** Retrieves a list of all available products from the database.
*   **Request Body:** None
*   **Response (Success):** `200 OK`
*   **Response Shape (Array of `ProductOut`):**
    ```json
    [
      {
        "id": 1,
        "name": "Monstera Deliciosa",
        "unit": "each",
        "cost_per_unit": 20.00,
        "price_per_unit": 45.99,
        "quantity_in_stock": 12.0
      }
    ]
    ```

#### 1.2 View Plant Details
*   **Method:** `GET`
*   **Path:** `/products/{product_id}`
*   **Description:** Retrieves details for a specific product using its database ID.
*   **Request Body:** None
*   **Response (Success):** `200 OK`
*   **Response Shape (`ProductOut`):**
    ```json
    {
      "id": 1,
      "name": "Monstera Deliciosa",
      "unit": "each",
      "cost_per_unit": 20.00,
      "price_per_unit": 45.99,
      "quantity_in_stock": 12.0
    }
    ```

#### 1.3 Add New Plant Inventory
*   **Method:** `POST`
*   **Path:** `/products/`
*   **Description:** Creates a new product catalog entry.
*   **Request Body (`ProductSchema`):**
    ```json
    {
      "name": "Fiddle Leaf Fig",
      "unit": "each",
      "cost_per_unit": 30.00,
      "price_per_unit": 60.00,
      "quantity_in_stock": 5.0
    }
    ```
    *(Note: `cost_per_unit` must be greater than 0, and `price_per_unit` must be greater than or equal to `cost_per_unit`. `quantity_in_stock` must be a float greater than or equal to 0.)*
*   **Response (Success):** `201 Created`
*   **Response Shape (`ProductOut`):**
    ```json
    {
      "id": 2,
      "name": "Fiddle Leaf Fig",
      "unit": "each",
      "cost_per_unit": 30.00,
      "price_per_unit": 60.00,
      "quantity_in_stock": 5.0
    }
    ```

#### 1.4 Reserve/Purchase a Plant
*   **Method:** `POST`
*   **Path:** `/products/{product_id}/reserve`
*   **Description:** Decrements stock by the requested quantity.
*   **Request Body:**
    ```json
    {
      "quantity": 2.0
    }
    ```
*   **Response (Success):** `200 OK`
*   **Response Shape (`ProductOut`):**
    ```json
    {
      "id": 1,
      "name": "Monstera Deliciosa",
      "unit": "each",
      "cost_per_unit": 20.00,
      "price_per_unit": 45.99,
      "quantity_in_stock": 10.0
    }
    ```

---

### 2. Error Handling

*   **Pydantic Validation (422 Unprocessable Entity):** Handled automatically by FastAPI if a user submits a payload violating `ProductSchema` constraints, such as a negative `cost_per_unit` or setting the `price_per_unit` lower than the cost.
*   **Business Logic (400 Bad Request):** If a user attempts to reserve a plant (Requirement 4) but requests a quantity greater than the current `quantity_in_stock`, the API must reject the transaction.
    ```json
    {
      "detail": "Insufficient stock. Requested: 2.0, Available: 1.0"
    }
    ```
*   **Not Found (404 Not Found):** Attempting to fetch or reserve a non-existent `product_id` must return `{"detail": "Product not found"}`.

---

### 3. Architecture & Separation of Concerns

*   **Data Validation (Inbound/Outbound):** Incoming request bodies for creation must be validated strictly against `ProductSchema`. Outbound data must be validated against `ProductOut` using the `response_model` argument in the route decorators.
*   **Database Interaction:** Handled by the `Product` SQLAlchemy ORM model, which maps to the `products` table. The Day 3 startup strategy, which synchronizes the schema using `Base.metadata.drop_all` and `Base.metadata.create_all`, remains intact in the main application module.
*   **Route/Controller Functions:** Must act purely as orchestrators. They will use the `db: Session = Depends(get_db)` dependency, execute business logic (like checking `quantity_in_stock`), mutate the model, and commit the transaction to the database.

---

### 4. API Design Decisions

**Payload Sizing Strategy: Unified Output Schema**
In the original spec, I proposed separate summary and detail schemas. I have revised this to use a single, unified output schema (`ProductOut`) for both the list and detail views. 

*   **Why:** The existing `Product` model and `ProductSchema` contain a very lean set of properties—only ID, name, unit, cost, price, and stock quantity. There are no heavy text fields (like long descriptions) or metadata to trim out.
*   **Client Benefit:** Using a unified schema reduces the maintenance burden on the backend by keeping Pydantic models DRY, while the payload size remains lightweight enough to not negatively impact client performance on grid views.