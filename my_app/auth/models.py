import jwt
import time

from werkzeug.security import generate_password_hash, check_password_hash 

from my_app import app, db 
 
class User(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(100)) 
    pwdhash = db.Column(db.String(500)) 
  
    def __init__(self, username, password): 
        self.username = username 
        self.pwdhash = generate_password_hash(password) 
  
    def check_password(self, password): 
        return check_password_hash(self.pwdhash, password)
    
    def generate_auth_token(self, expires_in = 600):
        return jwt.encode(
            { 'id': self.id, 'exp': time.time() + expires_in }, app.config['SECRET_KEY'], algorithm='HS256')
    
    @property
    def serialize(self):
       return {
           'id'    : self.id,
           'username'  : self.username
       }

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm=['HS256'])
        except:
            return
        return User.query.get(data['id'])
    
    @property
    def is_authenticated(self):
        return True 
    
    @property
    def is_active(self):
        return True 
    
    @property
    def is_anonymous(self):
        return False 
    
    def get_id(self):
        return str(self.id) 