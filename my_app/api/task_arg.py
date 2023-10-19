import json

from flask_restful import Resource, reqparse
from flask import request, abort

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name cannot be blank!')
parser.add_argument('category_id', type=int, required=True, help='Category cannot be blank!')

from my_app.tasks import operations


#  raise abort(500, message="Unable to determine domain permissions")
class TaskArgApi(Resource): 
 
    def get(self, id=None): 
        if not id: 
            tasks = operations.getAll() 
            res = {} 
            for task in tasks: 
                res[task.id] = { 
                    'name': task.name, 
                    'category': task.category.name
                } 
        else: 
            task = operations.getById(id)
            if not task: 
                abort(404) 
            res = json.dumps({ 
                'name': task.name, 
                'category': task.category.name
            }) 
        return res 
 
    def post(self):
        args = parser.parse_args()

 
        
        if len(args['name']) < 3:
            abort(400, {'message':"Name not valid"})

        task = operations.create(args['name'],args['category_id'])

        return task.serialize

    def put(self,id):
        task = operations.getById(id)  
        if not task:
            abort(400, {'message': 'Task not exits'})

        args = parser.parse_args()
            
        if len(args['name']) < 3:
            abort(400, message="Name not valid")
        
        operations.update(id, args['name'], args['category_id'])

        return task.serialize

    def delete(self,id):
        task = operations.getById(id)   
        if not task:
            abort(400, {'message': 'Task not exits'})
        
        operations.delete(id)

        return json.dumps({'message': 'Success'}) 

class TaskArgApiPaginate(Resource): 
 
    def get(self, page: int, per_page: int): 
        tasks = operations.pagination(page, per_page) 
        res = {} 
        for task in tasks: 
            res[task.id] = task.serialize

        return res