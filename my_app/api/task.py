import json

from my_app.tasks import operations
from my_app import config

from flask_restful import Resource 
from flask import request, abort

from werkzeug.utils import secure_filename

from my_app.documents import operations as doc_operations

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
            abort(403, {'message':"Sin parámetros"})
        
        form = request.form.to_dict()

        print(request.files.get("file"))

        if not "name" in request.form:
            abort(400, {'message': 'No name'})
        if len(request.form['name']) < 3:
            abort(400, {'message': 'No name'})

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
            abort(403, {'message': 'No form'})
        
        if not "name" in request.form:
            abort(400, {'message': 'No name'})
        if len(request.form['name']) < 3:
            abort(400, {'message': 'No name'})

        if not "category_id" in request.form:
            abort(400, {'message': 'No Category'})

        try:
            int(request.form['category_id'])
        except ValueError:
            abort(400, {'message': 'Category not valid'})
        
        operations.update(id, request.form['name'], request.form['category_id'])
     #https://stackoverflow.com/questions/28982974/flask-restful-upload-image
        
        # form2 = request.form.to_dict()
        # print(form2.files['file'])

        if request.files.get("file"):
            f = request.files.get("file")
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