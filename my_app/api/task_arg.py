import json

from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, abort, jsonify

import werkzeug

from my_app import config


from werkzeug.utils import secure_filename
from my_app.documents import operations as doc_operations


parser = reqparse.RequestParser()

parser.add_argument('name', required=True, help='Name cannot be blank!')
parser.add_argument('category_id', type=int, required=True, help='Category cannot be blank!')

from my_app.tasks import operations

nested_tag_fields = {
    'id': fields.String(),
    'name': fields.String()
}

task_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'category': fields.String(attribute=lambda x: x.category.name),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
}

#  raise abort(500, message="Unable to determine domain permissions")
class TaskArgApi(Resource): 
 
    @marshal_with(task_fields)
    # @jwt_required()
    def get(self, id=None): 
        if not id: 
            tasks = operations.getAll() 
            return tasks
        else: 
            task = operations.getById(id)
            if not task: 
                abort(404) 
            return task
 
    # @marshal_with(task_fields)
    @jwt_required
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

        if args['file']:
            f = args['file']
            if f and config.allowed_extensions_file(f.filename):
                filename = secure_filename(f.filename)
            
                document = doc_operations.create(filename, filename.lower().rsplit('.', 1)[1], f)
                operations.update(id, task.name, task.category_id, document.id)

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
    
class TaskArgUploadApi(Resource): 
    def put(self,id):
        task = operations.getById(id)  
        if not task:
            abort(400, {'message': 'Task not exits'})

        parserUpload = reqparse.RequestParser()
        parserUpload.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parserUpload.parse_args()

        if args['file']:
            f = args['file']
            if f and config.allowed_extensions_file(f.filename):
                filename = secure_filename(f.filename)
            
                document = doc_operations.create(filename, filename.lower().rsplit('.', 1)[1], f)
                operations.update(id, task.name, task.category_id, document.id)

        return task.serialize

import requests

# res = requests.post('http://127.0.0.1:5000/api/product', data=json.dumps(d), headers={'Content-Type': 'application/json'})
# res = requests.post('http://127.0.0.1:5000/api/product', headers={'Content-Type': 'application/json', "Authorization": "Bearer MYREALLYLONGTOKENIGOT"})

# res.json()