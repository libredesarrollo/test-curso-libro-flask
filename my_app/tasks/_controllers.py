import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

# from my_app.tasks.models import Task
from my_app import app
from my_app.tasks import forms
from my_app.tasks import models
from my_app.tasks import operations
from my_app.documents import operations as doc_operations

from my_app import config, cache

taskRoute = Blueprint('tasks',__name__, url_prefix="/tasks")

task_list =[]

@taskRoute.before_request
# @login_required
def before():
    pass


@taskRoute.route('/')
# @taskRoute.route('/<int:id>')
@cache.cached(timeout=60)
def index(): #page:int=1 
   return render_template('dashboard/task/index.html', tasks=operations.pagination(request.args.get('page', 1, type=int), request.args.get('size', 10, type=int)))

@taskRoute.route('/<int:id>')
def show(id:int):
   return "Show "+ str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    task=operations.getById(id)
    operations.delete(task.id)
   #  doc_operations.delete(task.document_id)
    return redirect(url_for('tasks.index'))


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
   print(form.name.errors)
   return render_template('dashboard/task/create.html', form=form)

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):

   # task = operations.getById(id)   
   task = models.Task.getById(id)
   form = forms.Task()#meta={'csrf':False}
   formTag = forms.TaskTagAdd()

   categories = [ (c.id, c.name) for c in models.Category.query.all()]
   form.category.choices = categories

   tags = [ (c.id, c.name) for c in models.Tag.query.all()]
   formTag.tag.choices = tags

   if request.method == 'GET':
      form.name.data = task.name
      form.category.data = task.category_id
   
   if form.validate_on_submit():
      operations.update(id, form.name.data, form.category.data)
      flash('The registry has been updated successfully', 'info')

      f = form.file.data
      if f and config.allowed_extensions_file(f.filename):
         filename = secure_filename(f.filename)
         
         document = doc_operations.create(filename, filename.lower().rsplit('.', 1)[1], f)
         operations.update(id, form.name.data, form.category.data, document.id)
         
   return render_template('dashboard/task/update.html', form=form, formTag=formTag, formTagDelete=forms.TaskTagRemove() ,task=task, id=id)


@taskRoute.route('/<int:id>/tag/add', methods=['POST'])
def tagAdd(id:int):

   formTag = forms.TaskTagAdd()
   tags = [ (c.id, c.name) for c in models.Tag.query.all()]
   formTag.tag.choices = tags

   if formTag.validate_on_submit():
      operations.addTag(id, formTag.tag.data)

   return redirect(url_for("tasks.update",id=id))

@taskRoute.route('/<int:id>/tag/delete', methods=['POST'])
def tagRemove(id:int):
   formTag = forms.TaskTagRemove()
   if formTag.validate_on_submit():
      operations.removeTag(id, formTag.tag.data)
      
   return redirect(url_for("tasks.update",id=id))