class Config(object): 
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost:3306/test_flask" 
 
class ProdConfig(Config): 
    pass 
 
class DevConfig(Config): 
    DEBUG = True 
    TESTING = True 