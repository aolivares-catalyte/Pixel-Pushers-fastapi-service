## Requierments

1. Connect postgres to our program
    - we as a product owner want to save products entered into our inventory to be able to retrieve later
        - we will need to change our routes to interact with a postgres database 

2. Create a route that retrieves all product information
    - we as a product ownwer want the ability to see all of our products
        - we need to change our route to retrieve a list of products already existing in our database

3. Create a route that retrieves a single product information
    - we as a product owner want to be able ro retrieve information on a single product
        - we need create a route for searching by name 
        - we need to create a route for searching by id number

4. Create a route for searchig for a product that doesnt existing
    - we as a product owner wants a certain reaction if someone searches for a product that doesnt existing
        - we need to create a response that informs the user that the item doesnt exist in our inventory

5. Create a response that only shows the user information that we want to display
    - we as a product owner want to create a response that filters certain information to be shown when requested
        - we need to create a schema for a product search response that shows certain data about the not all


### Allens comments:
Good job translating the requirments into technical requirments. You should add more about status and endpoints and explain why you made decsions about some fields.


---

Day-5

1. As a garden center manager I wanted to update existing products into the database so they will not delete and the final object update is varified 
    
    Now that the database has been connected save items into the database and be able to update them without error
              
               {
                    "status": "success",
                    "code": "200"
                    "message": "Product updated successfully.",
                    "data": {
                        "id": 01,
                        "name": "Red Roses",
                        "price": 29.99,
                        "stock_quantity": 45,
                        "is_active": true,
                        "updated_at": "2026-07-28T10:00:00Z"
                    }
                    }

                    
                      

2. As a garden center manager I want to be able to remove a product from inventory that has been discontinued
    
    Remove an item so employees or customers cant see it but keep previous sales data
                
                {
                "id": "01",
                "name": "Red Rose",
                "price": 29.99,
                "stock_quantity": 45,
                "is_active": true
                } ,
                
                {
                        "status": "success",
                        "code": "200"
                        "message": "Product discontinued successfully and removed from active inventory.",
                        "data": {
                            "id": 01,
                            "name": "Red Rose",
                            "price": 29.99,
                            "stock_quantity": 45,
                            "is_active": false
                        }
                }
                    :This will be more like a soft delete instead of deleting it permanatly it will make the product invisible to certain employees and customers


3. As a garden center manager I want to be able to see a clear message when deleting or updating an item that doesnt exist
    
    Create an endpoint that send out a clear error message when trying to update or delete non-existing product items

                
                {
                    "status": "success",
                    "message": "Item not found.",
                }
                                        
                    :This will be a clear message when a product is not found in the database


4. As a gardren center manager I want a clearly explain error message if there is an invalid entry
    
    If a person enters something like a negative number. I want a message to appear clearly explaining the invalid entry and not just an error code 

                            {
            "status": "error",
            "code": "422",
            "message": "Invalid Entry",
            "errors": [
                {
                "field": "price",
                "message": "Price must be a positive number greater than 0."
                }
            ]
            }

5. As a developer I want a clear and consistent response for every possible outcome successful or failure
    Test our code for every possible outcome and create a response that solves the results of each test





