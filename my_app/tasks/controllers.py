from flask import Blueprint, render_template, request, redirect, url_for, flash

from my_app.tasks.models import Task
from my_app.tasks import operations

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
   task_list.append(request.form.get('task')) #request.args.get('task')
   return render_template('dashboard/task/create.html')

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):
   task_list[id] = request.form.get('task') #request.args.get('task')
   return "Update "+ str(id)