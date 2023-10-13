from flask_restful import Resource 
from my_app import api 
 
class TaskApi(Resource): 
 
    def get(self, id=None): 
        # Return product data 
        return 'This is a GET response' 
 
    def post(self): 
        # Create a new product 
        return 'This is a POST response' 
 
    def put(self, id): 
        # Update the product with given id 
        return 'This is a PUT response' 
 
    def delete(self, id): 
        # Delete the product with given id 
        return 'This is a DELETE response' 