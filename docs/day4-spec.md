Requierments

1. Connect postgres to our program
        we as a product owner want to save products entered into our inventory to be able to retrieve later
            we will need to change our routes to interact with a postgres database 

2. Create a route that retrieves all product information
        we as a product ownwer want the ability to see all of our products
                we need to change our route to retrieve a list of products already existing in our database

3. Create a route that retrieves a single product information
        we as a product owner want to be able ro retrieve information on a single product
                we need create a route for searching by name 
                we need to create a route for searching by id number

4. Create a route for searchig for a product that doesnt existing
        we as a product owner wants a certain reaction if someone searches for a product that doesnt existing
                we need to create a response that informs the user that the item doesnt exist in our inventory

5. Create a response that only shows the user information that we want to display
        we as a product owner want to create a response that filters certain information to be shown when requested
                we need to create a schema for a product search response that shows certain data about the not all


Allens comments:
Good job translating the requirments into technical requirments. You should add more about status and endpoints and explain why you made decsions about some fields.