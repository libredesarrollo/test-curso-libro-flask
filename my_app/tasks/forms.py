from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, FileField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    document = FileField('File') 
    # price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    # category_id = SelectField('Categoría', coerce=int)
    # file = FileField('Archivo') #, validators=[FileRequired()]