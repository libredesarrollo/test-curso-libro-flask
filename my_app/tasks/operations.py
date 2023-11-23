from sqlalchemy.orm import Session
# from sqlalchemy. import 
# get_or_404

from my_app.tasks import models
from my_app import db, cache

# @cache.memoize(60)
@cache.cached(timeout=60, key_prefix='last_task') 
def getById(id: int):
    task = db.session.query(models.Task).filter(models.Task.id == id).first()
    # task = models.Task.query.get_or_404(id)  
    
    # get_or_404(models.Task,id)
    # task = db.session.query(models.Task).get(id)
    # db.session.get(models.Task, id)
    # task = db.session.query.  #query.get_or_404(models.Task,ident=id) 
    task = db.session.get(models.Task, id)
    
    return task

@cache.cached(timeout=60, key_prefix='last_task') 
def getLastTask():
    task = models.Task.query.order_by(models.Task.id.desc()).first()
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

@cache.cached(timeout=7200, key_prefix='pagination_data') 
def pagination(page:int=1, per_page:int=10):
    return models.Task.query.paginate(page=page, per_page=per_page)

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