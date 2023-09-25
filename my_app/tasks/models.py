from sqlalchemy.orm import relationship

from my_app import db

task_tag = db.Table('task_tag', 
        db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'),primary_key=True),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'),primary_key=True)
        )

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
        nullable=False)
    tags = relationship('Tag', secondary=task_tag, back_populates='tasks')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    tasks = relationship('Task', secondary=task_tag)