from sqlalchemy.orm import relationship

from my_app.documents.models import Document

from my_app import db

task_tag = db.Table('task_tag', 
        db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'),primary_key=True),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'),primary_key=True)
        )

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'),
        nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
        nullable=False)
    tags = relationship('Tag', secondary=task_tag, back_populates='tasks')
    category = relationship('Category')

    document = relationship('Document', lazy='joined')

    def getById(self, id: int):
        task = db.session.query(self).filter(id == id).first()
        return id

    @property
    def serialize(self):
       return {
           'id'    : self.id,
           'name'  : self.name,
           'category'  : self.category.name,
           'category_id'  : self.category_id,
       }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    tasks = relationship('Task', secondary=task_tag)