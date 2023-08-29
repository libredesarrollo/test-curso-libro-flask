# from flask import Flask 
# from config import DevConfig 
 
# app = Flask(__name__) 
# app.config.from_object(DevConfig) 
 
# @app.route('/') 
# def home(): 
#     return '<h1>Hello World!</h1>' 
 
# if __name__ == '__main__': 
#     app.run() 

from flask import Flask 
app = Flask(__name__) 
 
@app.route('/') 
def hello_world(): 
    return 'Hello to the World of Flask!' 


if __name__ == '__main__': 
    app.run() 
