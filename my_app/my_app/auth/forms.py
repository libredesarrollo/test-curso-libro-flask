
from flask_wtf import FlaskForm 
from wtforms import TextField, PasswordField 
from wtforms.validators import InputRequired, EqualTo 

class RegistrationForm(FlaskForm): 
    username = TextField('Username', [InputRequired()]) 
    password = PasswordField( 
        'Password', [ 
            InputRequired(), EqualTo('confirm', message='Passwords must match') 
        ] 
    ) 
    confirm = PasswordField('Confirm Password', [InputRequired()]) 
 
class LoginForm(FlaskForm): 
    username = TextField('Username', [InputRequired()]) 
    password = PasswordField('Password', [InputRequired()]) 