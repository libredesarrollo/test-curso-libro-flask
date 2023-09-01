from sqlalchemy.orm import Session

from my_app.tasks import models
from my_app import db


def getById(id: int):
    # task = db.session.query(models.Task).filter(models.Task.id == id).first()
    task = models.Task.query.get_or_404(id)  
    # task = db.session.query(models.Task).get(id)
    return task

def getAll():
    tasks = db.session.query(models.Task).all()
    return tasks 

def create(name: str):
    taskdb = models.Task(name=name)
    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def update(id: int, name: str):
    taskdb = getById(id=id)
    taskdb.session.name = name

    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def delete(id: int):  
    task = getById(id=id)  
    db.session.delete(task)
    db.session.commit()

def paginate(page:int, size:int):
    models.Task.query.paginate(page,size)
