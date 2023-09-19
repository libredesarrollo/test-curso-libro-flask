import os

ALLOWED_EXTENSIONS_FILES = {'pdf','jpg','jpeg','gif','png'}

def allowed_extensions_file(filename):
   return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_FILES

class Config(object): 
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost:3306/test_flask" 
    SECRET_KEY="SECRETKEY" 
    UPLOAD_FOLDER=os.path.realpath('.') + '/my_app/uploads'
 
class ProdConfig(Config): 
    pass 
 
class DevConfig(Config): 
    DEBUG = True 
    TESTING = True 