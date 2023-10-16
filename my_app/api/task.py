import json

from my_app.tasks import operations

from flask_restful import Resource 
from flask import request, abort

#  raise abort(500, message="Unable to determine domain permissions")
class TaskApi(Resource): 
 
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

        if not request.form:
            abort(403, message="Sin parámetros")
        

        if not "name" in request.form:
            abort(400, {'message': 'No name'})
        if len(request.form['name']) < 3:
            abort(400, message="Name not valid")

        if not "category_id" in request.form:
            abort(400, {'message': 'No Category'})

        try:
            int(request.form['category_id'])
        except ValueError:
            abort(400, {'message': 'Category not valid'})

        task = operations.create(request.form['name'],request.form['category_id'])

        return task.serialize

    def put(self,id):
        task = operations.getById(id)  
        if not task:
            abort(400, {'message': 'Task not exits'})

        if not request.form:
            abort(403, message="No params")
        
        if not "name" in request.form:
            abort(400, {'message': 'No name'})
        if len(request.form['name']) < 3:
            abort(400, message="Name not valid")

        if not "category_id" in request.form:
            abort(400, {'message': 'No Category'})

        try:
            int(request.form['category_id'])
        except ValueError:
            abort(400, {'message': 'Category not valid'})
        
        operations.update(id, request.form['name'], request.form['category_id'])

        return task.serialize

    def delete(self,id):
        task = operations.getById(id)   
        if not task:
            abort(400, {'message': 'Task not exits'})
        
        operations.delete(id)

        return json.dumps({'message': 'Success'}) 