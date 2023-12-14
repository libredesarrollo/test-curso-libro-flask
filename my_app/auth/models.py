import jwt
import time

from werkzeug.security import generate_password_hash, check_password_hash 
from sqlalchemy.orm import relationship

from my_app import app, db 
 
class User(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(100)) 
    pwdhash = db.Column(db.String(500)) 

    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    avatar_id = db.Column(db.Integer, db.ForeignKey('documents.id'),
        nullable=True)
    avatar = relationship('Document', lazy='joined')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'),
        nullable=True)
    address = relationship('Address', lazy='joined')

    social_networks = db.relationship('SocialNetwork', secondary='user_social_networks')

  
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
    
    # Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class SocialNetwork(db.Model):
    __tablename__ = 'social_networks'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserSocialNetwork(db.Model):
    __tablename__ = 'user_social_networks'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    social_network_id = db.Column(db.Integer(), db.ForeignKey('social_networks.id', ondelete='CASCADE'))

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.String(250), unique=True)