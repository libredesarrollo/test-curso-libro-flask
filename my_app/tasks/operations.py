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

def create(name: str, category_id:int):
    taskdb = models.Task(name=name, category_id=category_id)
    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def update(id: int, name: str, category_id:int, document_id:int = None):
    taskdb = getById(id=id)
    taskdb.name = name
    taskdb.category_id = category_id
    if document_id is not None:
        taskdb.document_id = document_id

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

#tag
def addTag(id: int, tagid: int):
    task = getById(id=id)
    tag = models.Tag.query.get_or_404(tagid)
    task.tags.append(tag)

    db.session.add(task)
    db.session.commit()
    return task

def removeTag(id: int, tagid: int):
    task = getById(id=id)
    task = getById(id)
    tag = models.Tag.query.get_or_404(tagid)
    task.tags.remove(tag)

    db.session.add(task)
    db.session.commit()
    return task