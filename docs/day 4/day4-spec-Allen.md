# Day 4 Technical Requirements Spec

## API Contract Summary

### Endpoints That Satisfy the Business Requirements

- POST /products
  - Purpose: Persist a new product.
- GET /products
  - Purpose: View the full catalog.
- GET /products/{product_id}
  - Purpose: Look up one specific product by identifier.
- GET /products/search?name={name}&unit={unit}
  - Purpose: Search for products by name and optional unit.

### Request Body Shape

- POST /products request body (ProductCreate):
`json   {       "name": "Basil Plant",       "unit": "each",       "cost_per_unit": 1.25,       "price_per_unit": 2.5,       "quantity_in_stock": 40   }`   
- GET /products, GET /products/{product_id}, and GET /products/search do not use a request body.



### Successful Response Shapes

- POST /products
  - Status: 201 Created
  - Body:
  `json   {       "id": 101,       "name": "Basil Plant",       "unit": "each",       "cost_per_unit": 1.25,       "price_per_unit": 2.5,       "quantity_in_stock": 40   }`
- GET /products
  - Status: 200 OK
  - Body (non-empty):
  `json   {       "message": "Products retrieved successfully",       "products": [           {               "id": 101,               "name": "Basil Plant",               "unit": "each",               "cost_per_unit": 1.25,               "price_per_unit": 2.5,               "quantity_in_stock": 40           }       ]   }`   
  - Body (empty list):
  `json   {       "message": "No products found",       "products": []   }`
- GET /products/{product_id}
  - Status: 200 OK
  - Body:
  `json   {       "id": 101,       "name": "Basil Plant",       "unit": "each",       "cost_per_unit": 1.25,       "price_per_unit": 2.5,       "quantity_in_stock": 40   }`
- GET /products/search?name={name}&unit={unit}
  - Status: 200 OK
  - Body (matches found):
  `json   {       "message": "Matching products found",       "results": [           {               "id": 101,               "name": "Basil Plant",               "unit": "each",               "cost_per_unit": 1.25,               "price_per_unit": 2.5,               "quantity_in_stock": 40           }       ]   }`   
  - Body (no matches):
  `json   {       "message": "No matching products found",       "results": []   }`



### Failure Response for Requirement 4 (Product Not Found by ID)

- Endpoint: GET /products/{product_id}
- When product does not exist:
  - Status: 404 Not Found
  - Body:
  `json   {       "detail": "Product not found"   }`



### Responsibility Split: Validation vs Database vs Route Logic

- Pydantic schema (ProductCreate):
  - Validates incoming request data and constraints.
  - Invalid input is rejected with 422 before route logic proceeds.
- SQLAlchemy model (Product):
  - Maps Python objects to the products table columns.
  - Represents persisted database records.
- Route functions + dependency (get_db):
  - Receive validated request data.
  - Perform query/filter/create actions using SQLAlchemy and session.
  - Handle commit/refresh on writes and return response payloads.



### Returned Fields Decision and Rationale

- ProductRead fields returned:
  - id
  - name
  - unit
  - cost_per_unit
  - price_per_unit
  - quantity_in_stock
- Why these fields:
  - They are the business fields needed by clients for catalog display, stock checks, and margin awareness.
  - id is required for stable single-item lookup and client-side linking.
  - Returning only schema-defined fields prevents ORM/session internals from leaking and keeps the API contract predictable.



## Technical Specs



### 1. Store Product Objects in Postgres

Given a validated SQLAlchemy Product instance, when the application is connected to the Postgres database through the get_db session dependency, the instance must be added to the session, committed, and refreshed. The resulting record must be permanently stored in the products table and returned to the client using ProductRead.

- The persistence operation occurs inside the POST /products endpoint.
- The endpoint converts a validated Pydantic ProductCreate into a SQLAlchemy Product.
- The database write flow is open session, add, commit, refresh, return.
- Errors:
  - Validation errors return 422.
  - Database failures return 500.
- Response:
  - 201 Created with ProductRead.
  - No SQLAlchemy objects are returned directly.



### 2. List All Products

When a client performs a GET /products request, the service queries the Postgres products table using the SQLAlchemy session provided by get_db. The endpoint returns 200 OK with a response object that follows ProductListResponse and contains a message and a list of ProductRead objects.

- Endpoint: GET /products
- Database interaction:
  - Use db.query(Product).all().
  - No filtering and no pagination for Day 4.
- Response shape:
  - 200 OK
    - Body (non-empty):
    - Body (empty):
- Empty catalog behavior:
  - Return 200 OK.
  - Return products as an empty list.
  - Return message as "No products found".



### 3. Get Product by ID

When a client performs a GET /products/{product_id} request, the service queries the products table by primary key. If the product exists, return 200 OK with a single ProductRead object. If the product does not exist, return 404 Not Found with a clear message.

- Endpoint: GET /products/{product_id}
- Path parameters:
  - product_id: int
- Response behavior:
  - Found: 200 OK with ProductRead.
  - Not found: 404 Not Found with a message such as "Product not found".



### 4. Search Products by Name and Optional Unit

When a client performs a GET /products/search request with query parameters, the service returns matching products from Postgres. Search responses always use list semantics and never return 404 for no matches.

- Endpoint: GET /products/search?name={name}&unit={unit}
- Query parameters:
  - name: str (required)
  - unit: Optional[str] (default: "each")
- Search logic:
- Response shape:
  - 200 OK
    - Body (matches found):
    - Body (no matches):
- Empty search behavior:
  - Return 200 OK.
  - Return results as an empty list.
  - Return message as "No matching products found".



### 5. Response Model Enforcement

All product endpoints must return Pydantic response models rather than raw SQLAlchemy objects.

- ProductRead is the response schema for returning one product object.
- Endpoint mapping:
  - POST /products -> ProductRead
  - GET /products/{product_id} -> ProductRead
  - GET /products -> ProductListResponse
  - GET /products/search -> message + list of ProductRead
- SQLAlchemy objects must be serialized through Pydantic before returning.



### 6. Database Session Dependency

All product endpoints must use the get_db FastAPI dependency to obtain a database session. Route handlers must not manually create sessions.

- Use: db: Session = Depends(get_db)
- Dependency responsibilities:
  - Open and close the session.
- Route responsibilities:
  - Execute query logic.
  - Commit for successful writes.
  - Roll back when write operations fail.
- Benefits:
  - Prevents connection leaks.
  - Keeps transaction handling explicit and consistent.



### 7. Input Validation

All incoming product creation requests must be validated using ProductCreate. Invalid data must return 422 Unprocessable Entity from FastAPI/Pydantic.

- Validation:
  - Pydantic enforces field types and constraints.
- Error behavior:
  - FastAPI automatically returns 422 with validation details.
- Conversion:
  - Validated ProductCreate is converted to SQLAlchemy Product before persistence.



### 8. Consistent API Shape

All product endpoints must follow a predictable response contract.

- Single-resource endpoints return one object:
  - POST /products -> ProductRead
  - GET /products/{product_id} -> ProductRead
- List endpoints return an object with a message and a list:
  - GET /products -> { message, products: [...] }
  - GET /products/search -> { message, results: [...] }
- Empty list responses are explicit and informative:
  - products: [] with message "No products found"
  - results: [] with message "No matching products found"
- No null list fields and no mixed object-or-list return types.



### 9. No SQLAlchemy Leakage

The API must never return raw SQLAlchemy model instances, session-bound objects, or ORM-specific fields.

- SQLAlchemy internals such as _sa_instance_state must never appear in response payloads.
- Use ProductRead for product serialization.
- Ensures:
  - Clean JSON
  - Stable API contract
  - No accidental exposure of internal implementation details



## List of Business Requirements

1. Persist New Products

As a garden center manager, I want new products to be permanently saved when they are added to the system, so that the catalog does not disappear every time the server restarts.

1. View the Full Catalog

As a garden center employee, I want to see a list of every product currently in the system, so that I can review what is in stock.

1. Look Up a Single Product

As a garden center employee, I want to look up one specific product by its identifier, so that I can quickly check details without scanning the entire catalog.

1. Search Products and See Clear Empty Results

As a garden center employee, I want a clear message when no products match my catalog or search request, so that I can tell the difference between an empty result and a failure.

1. API Responses Do Not Leak Implementation Details

As the garden center technology partner, I want the data returned by the API to be intentional and controlled, so that the API has a stable and predictable contract regardless of internal database structure.

---



# Day 5 Technical Requirements Spec

### Endpoints That Satisfy the Business Requirements

- PUT /items/{id}
  - Purpose: Make changes to an existing product.
- DELETE /items/{id}
  - Purpose: Remove a product from the database.

### Request Body Shape

- PUT /items/{id}:
`json   {"id": 10, "name": "Basil Plant",       "unit": "each",       "cost_per_unit": 1.25,       "price_per_unit": 2.5,       "quantity_in_stock": 40   }`   
- DELETE /items/{id} do not use a request body.

## Successful Response Shapes

- PUT /items/{id}
  - Status: 200 OK (Successful update)
  - Body:
  `json   {   "message": "Product Has been updated successfully",  "id": 101,       "name": "Basil Plant",       "unit": "each",       "cost_per_unit": 1.25,       "price_per_unit": 2.5,       "quantity_in_stock": 40   }`
- DELETE /items/{id}
  - Status: 204 No content (Successful Delete)
  - Body (non-empty):
  `json   {       "message": "Product Has been deleted successfully",       "product": [           {               "id": 101,               "name": "Basil Plant",               "unit": "each",               "cost_per_unit": 1.25,               "price_per_unit": 2.5,               "quantity_in_stock": 40           }       ]   }`   
  

### Failure Response (Product Not Found by ID)

- Endpoint: PUT /items/{id}
- When product was not found:
  - Status: 404 Not Found
  - Body:
  `json   {       "detail": "Product not found"   }`
  - Endpoint: DELETE /items/{id}
- When product was not found:
  - Status: 404 Not Found
  - Body:
  `json   {       "detail": "Product not found"   }`





### Returned Fields Decision and Rationale

- ProductUpdate fields returned:
  - id
  - name
  - unit
  - cost_per_unit
  - price_per_unit
  - quantity_in_stock
- Why these fields:
  - These are the specific details the garden center manager needs to modify so that the catalog reflects reality without needing to delete and recreate the item.
  -The endpoint must retain its response_model to enforce the output shape. This ensures every outcome has a predictable, documented contract for anyone integrating with the API



## Technical Specs



### Update Endpoint (PUT /products/{id})

-Method & Path: PUT /products/{id}. 
-Request Body: A JSON payload governed by the Pydantic schema containing product fields such as price, cost, stock, and name.  -Success Response: Returns a 200 status code with the updated product body, utilizing the established response_model.  
-Failure Response (Not Found): If the target ID does not exist, the API returns a 404 Not Found status code with a clear error message in the body. 
-Failure Layer: The "not found" failure is caught via a manual check in the route, triggering an HTTPException to prevent an unhandled 500 server error.



### Delete Endpoint (DELETE /products/{id})

1. Method & Path: DELETE /products/{id}.  
2. Success Response: Returns a 204 status code with no response body.  
3. Failure Response (Not Found): If the target ID does not exist, the API returns a 404 Not Found status code with a clear error message in the body.  
4. Failure Layer: Similar to the update endpoint, the "not found" failure is caught via a manual check in the route, triggering an HTTPException.  

### Pydantic-Level Data Validation
1. Validation Rules: At least one custom validation rule is added directly into the Pydantic schema (e.g., product price must be greater than 0). Because this is at the schema level, this rule inherently applies to both the existing Create endpoint and the new Update endpoint.  
2. Failure Response (Invalid Input): Violating the validation rule results in a 422 Unprocessable Entity status code. The response body contains a readable explanation of the error rather than a raw stack trace. 
3. Failure Layer: Invalid data failures are caught immediately by Pydantic validation before the request ever reaches the route logic or the database layer.  




1.Update an Existing Product

As a garden center manager, I want to update a product's details (price, cost, stock, name) after it's been created, so that the catalog reflects reality without needing to delete and recreate the item.

2.Remove a Discontinued Product

As a garden center manager, I want to permanently remove a product from the catalog, so that discontinued items no longer show up for staff or customers.

3.Clear Failure When Updating or Deleting Something That Doesn't Exist

As a garden center employee, I want a clear, correct response when I try to update or delete a product that isn't in the system, so that I know immediately it wasn't found rather than getting a server error or a false success.

4.Reject Invalid Data Before It Reaches the Database

As the garden center's technology partner, I want obviously invalid input (like a negative price) rejected immediately with a readable explanation, so that bad data never gets a chance to corrupt the catalog and staff aren't left guessing what went wrong.

5.A Predictable, Documented Contract for Every Outcome

As the garden center's technology partner, I want every endpoint's possible responses, success and failure, documented and verifiable, so that anyone integrating with this API knows exactly what to expect in every case.