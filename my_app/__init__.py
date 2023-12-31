from flask import Flask, session

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cli import FlaskCLI
from flask_caching import Cache
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension

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


#cache
cache = Cache()
cache.init_app(app)

#debug
toolbar = DebugToolbarExtension(app)

#Mail
# # # from flask_mail import Mail, Message
# # # mail = Mail()
# # # mail.init_app(app)

# # # def send_email():
# # #     msg = Message(body="Text Example", 
# # #                   sender="no-reply@desarrollolibre.net",
# # #                   recipients=["andres29111990@gmail.com"], subject="Subject")
# # #     try:
# # #         print(mail.send(msg))
# # #     except Exception as e:
# # #         print(e)
# # # with app.app_context():
# # #     send_email()

# blueprints
from my_app.auth.controllers import authRoute 
from my_app.tasks.controllers import taskRoute 
# import my_app.tasks.controllers
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

@app.route('/test/session/check')
def test_session_check():
    if 'username' in session:
        return 'Logged in as '+session["username"]
    return 'You are not logged in'


@app.route('/test/session/set')
def test_session_set():
    session['username'] = 'user'
    return 'Test'


@app.route('/test/session/pop')
def test_session_pop():
    session.pop('username', None)
    return 'Test'



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

#Babel



def get_locale():
    # return 'es'
    return request.accept_languages.best_match(['es', 'en'])

babel = Babel(app, locale_selector=get_locale)

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

ALLOWED_LANGUAGES = { 
   'en': 'English', 
   'es': 'Spanish', 
} 


