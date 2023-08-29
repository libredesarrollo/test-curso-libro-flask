from flask import Flask 
from my_app.tasks.controllers import taskRoute 
 
from my_app.config import DevConfig 
 
app = Flask(__name__)
app.config.from_object(DevConfig) 

from flask import render_template, request 


@app.route('/') 
@app.route('/hello') 
def hello_world(): 
    name = request.args.get('name', 'DesarrolloLibre') 
    return render_template('index.html', name=name)


app.register_blueprint(taskRoute) 

