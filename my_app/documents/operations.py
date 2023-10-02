from sqlalchemy.orm import Session

from my_app.documents import models
from my_app import db

def create(name: str, ext: str):
    document = models.Document(name=name, ext=ext)
    db.session.add(document)
    db.session.commit()
    db.session.refresh(document)
    return document