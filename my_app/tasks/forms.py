from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, FileField, DateField, HiddenField
from wtforms.validators import InputRequired, ValidationError

def my_length_check(form, field):
    if len(field.data) > 1:
        raise ValidationError('Field must be less than 50 characters')

def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min and l > max:
            field.errors += (ValidationError(message=message),)
            raise ValidationError(message=message)

    return _length

class Task(FlaskForm):
    
    # name = StringField('Name', [InputRequired(), length(max=50)]) # length(max=50)]
    # name = StringField('Name', [InputRequired(), length(max=1)])
    name = StringField('Name', validators=[InputRequired(), length(max=1)]) # length(max=50)]
    # document = FileField('File') 
    # date = DateField('Date',  format='%Y-%m-%d')
    # language = SelectField('Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    category = SelectField('Category',)
    # price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    # category_id = SelectField('Categoría', coerce=int)
    file = FileField('Archivo') #, validators=[FileRequired()]

    # def validate_name(form, field):
    #     if len(field.data) > 2:
    #         raise ValidationError('Name must be less than 2 characters')


class TaskTagAdd(FlaskForm):
   tag = SelectField('Tag',)

class TaskTagRemove(FlaskForm):
   tag = HiddenField('Tag')