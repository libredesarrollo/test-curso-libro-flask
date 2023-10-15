import json

from my_app import api 
from my_app.tasks import operations

from flask_restful import Resource 
from flask import request, abort

#  raise abort(500, message="Unable to determine domain permissions")
class TaskApi(Resource): 
 
    def get(self, id=None, page=1): 
        if not id: 
            tasks = operations.pagination(page) 
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
        p = Product.query.get(id)   
        if not p:
            return sendResJson(None,"Producto no existe",403)

        if not request.form:
            return sendResJson(None,"Sin parámetros",403)
        
        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"Sin parámetro nombre",403)
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no válido",403)

        #validaciones precio
        if not "price" in request.form:
            return sendResJson(None,"Sin parámetro precio",403)

        try:
            float(request.form['price'])
        except ValueError:
            return sendResJson(None,"Precio no válido",403)

        #validaciones category_id
        if not "category_id" in request.form:
            return sendResJson(None,"Sin parámetro categoría",403)

        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None,"Categoría no válida",403)

        #if request.form['price'] is not float:
            #return "Precio no válido",403

        p.name = request.form['name']
        p.price = request.form['price']
        p.category_id = request.form['category_id']
        
        db.session.add(p)
        db.session.commit()

        return sendResJson(productToJson(p),None,200)

    def delete(self,id):
        product = Product.query.get(id)   
        if not product:
            return sendResJson(None,"Producto no existe",403)
        
        db.session.delete(product)
        db.session.commit()

        return sendResJson("Producto eliminado",None,200)