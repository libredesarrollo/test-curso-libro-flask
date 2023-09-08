from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template, request 

from my_app.config import DevConfig 
 
app = Flask(__name__)
app.config.from_object(DevConfig) 

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test_flask'
#load configuration
db=SQLAlchemy(app)
migrate = Migrate(app, db)
# blueprints
from my_app.tasks.controllers import taskRoute 
app.register_blueprint(taskRoute) 

# final process
# with app.app_context():
#     db.create_all()

# routes
@app.route('/') 
@app.route('/hello') 
def hello_world(): 
    name = request.args.get('name', 'DesarrolloLibre') 
    return render_template('index.html', name=name)