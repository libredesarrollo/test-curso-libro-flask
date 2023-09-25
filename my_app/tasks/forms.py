from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, FileField, DateField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    # document = FileField('File') 
    # date = DateField('Date',  format='%Y-%m-%d')
    # language = SelectField('Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    category = SelectField('Category',)
    # price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    # category_id = SelectField('Categoría', coerce=int)
    # file = FileField('Archivo') #, validators=[FileRequired()]


class TaskTag(FlaskForm):
   tag = SelectField('Tag',)