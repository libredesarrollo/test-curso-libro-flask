from flask import Blueprint, render_template, request, redirect, url_for, flash

from my_app.tasks.models import Task

taskRoute = Blueprint('tasks',__name__, url_prefix="/tasks")

@taskRoute.route('/')
# @taskRoute.route('/<int:id>')
def index(): #page:int=1
    Task
    return "Index"

@taskRoute.route('/<int:id>')
def show(id:int):
   return "Show "+ str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
   return "Delete "+ str(id)

@taskRoute.route('/create', methods=('GET', 'POST'))
def create():
   return "Create"

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):
   return "Update "+ str(id)