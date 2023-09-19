import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# from my_app.tasks.models import Task
from my_app import app
from my_app.tasks import forms
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
   if form.validate_on_submit():
      operations.create(form.name.data)
      print(config.allowed_extensions_file(form.document.data.filename))
      if form.document.data and config.allowed_extensions_file(form.document.data.filename):
         print(form.document.data)
         f = form.document.data
         filename = secure_filename(f.filename)
         f.save(os.path.join(
            app.instance_path, app.config['UPLOAD_FOLDER'], filename
         ))
     
   return render_template('dashboard/task/create.html', form=form)

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):
   task_list[id] = request.form.get('task') #request.args.get('task')
   return "Update "+ str(id)