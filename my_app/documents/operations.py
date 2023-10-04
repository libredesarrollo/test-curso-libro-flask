import os

from sqlalchemy.orm import Session

from my_app.documents import models
from my_app import db, app

def getById(id: int):
    document = db.session.query(models.Document).get(id)
    return document

def create(name: str, ext: str, file = None):
    document = models.Document(name=name, ext=ext)
    db.session.add(document)
    db.session.commit()
    db.session.refresh(document)

    if file is not None:
        file.save(os.path.join(
            app.instance_path, app.config['UPLOAD_FOLDER'], name
        ))

    return document

def delete(id: int):  
    document = getById(id=id)
    os.remove(app.instance_path, app.config['UPLOAD_FOLDER'], document.name)
    db.session.delete(document.name)
    db.session.commit()

