import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# from my_app.tasks.models import Task
from my_app import app
from my_app.tasks import forms
from my_app.tasks import models
from my_app.tasks import operations

from my_app import config

taskRoute = Blueprint('tasks',__name__, url_prefix="/tasks")

task_list =[]

@taskRoute.route('/')
# @taskRoute.route('/<int:id>')
def index(): #page:int=1
    return render_template('dashboard/task/index.html',tasks=task_list)

@taskRoute.route('/<int:id>')
def show(id:int):
   return "Show "+ str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
   del task_list[id] 
   return "Delete "+ str(id)

@taskRoute.route('/create', methods=('GET', 'POST'))
def create():

   # form = forms.Task(csrf_enabled=False)
   form = forms.Task()
   categories = [ (c.id, c.name) for c in models.Category.query.all()]
   form.category.choices = categories
   # print(form.date.data)
   if form.validate_on_submit():
      operations.create(form.name.data, form.category.data)
      # print(config.allowed_extensions_file(form.document.data.filename))
      # if form.document.data and config.allowed_extensions_file(form.document.data.filename):
      #    print(form.document.data)
         # f = form.document.data
         # filename = secure_filename(f.filename)
         # f.save(os.path.join(
         #    app.instance_path, app.config['UPLOAD_FOLDER'], filename
         # ))
     
   return render_template('dashboard/task/create.html', form=form)

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):

   task = operations.getById(id)   
   form = forms.Task()#meta={'csrf':False}
   formTag = forms.TaskTag(meta={'csrf':False})

   categories = [ (c.id, c.name) for c in models.Category.query.all()]
   form.category.choices = categories

   tags = [ (c.id, c.name) for c in models.Tag.query.all()]
   formTag.tag.choices = tags

   if request.method == 'GET':
      form.name.data = task.name
      form.category.data = task.category_id
   
   if form.validate_on_submit():
      operations.update(form.name.data, form.category.data)
   return render_template('dashboard/task/update.html', form=form, formTag=formTag)


@taskRoute.route('/<int:id>/tag/<int:tagid>/add', methods=['POST'])
def tagAdd(id:int, tagid:int):

   operations.addTag(id, tagid)
   return redirect(url_for("tasks.update",id=id))

@taskRoute.route('/<int:id>/tag/<int:tagid>/delete', methods=['POST'])
def tagRemove(id:int, tagid:int):

   operations.removeTag(id, tagid)
   return redirect(url_for("tasks.update",id=id))