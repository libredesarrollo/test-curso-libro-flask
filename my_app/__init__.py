from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cli import FlaskCLI

from flask import render_template, request 

from my_app.config import DevConfig

 
app = Flask(__name__, static_folder='assets')
app.config.from_object(DevConfig) 

FlaskCLI(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test_flask'
#load configuration
db=SQLAlchemy(app)
migrate = Migrate(app, db)

#login
login_manager = LoginManager() 
login_manager.init_app(app) 
# login_manager.login_view = 'auth.login' 


jwt = JWTManager()
jwt.init_app(app)

# blueprints
from my_app.auth.controllers import authRoute 
from my_app.tasks.controllers import taskRoute 
app.register_blueprint(authRoute) 
app.register_blueprint(taskRoute) 



# final process
# with app.app_context():
#     db.create_all()

# routes
@app.route('/') 
@app.route('/hello') 
def hello_world(): 
    name = request.args.get('name', 'DesarrolloLibre') 
    return {'hello': 'world'}
    # return render_template('index.html', name=name)


#api
from my_app.api.task import TaskApi
from my_app.api.task_arg import TaskArgApi, TaskArgUploadApi, TaskArgApiPaginate
api = Api(app)

# api.add_resource(TaskApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskArgApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskArgUploadApi, '/api/task/upload/<int:id>')
api.add_resource(TaskArgApiPaginate, '/api/task/paginate/<int:page>/<int:per_page>')

# extensions
from my_app.comands.user import register
register(app)