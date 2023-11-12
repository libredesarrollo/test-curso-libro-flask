
import json

from my_app.tasks import operations
from my_app.auth.models import User

from flask_jwt_extended import create_access_token

def test_create(app, client):

    dataform = {
        "name": "andres",
        "category_id": 1
    }

    tasksCount=0
    with app.app_context():
        tasksCount = len(operations.getAll())
        response =  client.post("/api/task", json=dataform)
        assert response.status_code == 200

        assert len(operations.getAll()) == tasksCount+1
        lastTask = operations.getLastTask()
        assert lastTask.name == response.get_json()['name']
        assert lastTask.id == response.get_json()['id']

def test_create_auth(app, client):

    dataform = {
        "name": "andres",
        "category_id": 1
    }

    tasksCount=0
    with app.app_context():
        tokenauth = create_access_token(identity=User.query.filter_by(username='admin').first().id)
        headers = { "Authorization": "Bearer "+tokenauth }
        # print(tokenauth)
        # assert True == False
        tasksCount = len(operations.getAll())
        response =  client.post("/api/task", json=dataform, headers=headers)
        assert response.status_code == 200

        assert len(operations.getAll()) == tasksCount+1
        lastTask = operations.getLastTask()
        assert lastTask.name == response.get_json()['name']
        assert lastTask.id == response.get_json()['id']


def test_update(app, client):
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.get('/tasks/update/'+str(lastTask.id))

        assert response.status_code == 200
        assert '<input id="name" name="name" required type="text" value="'+lastTask.name+'">' in response.get_data(as_text=True)

        dataform = {
            "name": "new Task",
            "category": 1
        }

        response =  client.post("/tasks/update/"+str(lastTask.id), data=dataform)

        assert response.status_code == 200
        assert '<input id="name" name="name" required type="text" value="'+dataform.get('name')+'">' in response.get_data(as_text=True)

        task = operations.getById(lastTask.id)

        assert task.name == dataform.get('name') and task.category_id == dataform.get('category')

from flask import jsonify 

def test_index(app, client):
    with app.app_context():
        response = client.get('/api/task')
        assert response.status_code == 200
        tasks = operations.getAll()
        for i in range(len(tasks)):
            assert tasks[i].name == response.get_json()[i]['name']

def test_show(app, client):
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.get('/api/task/'+str(lastTask.id))
        assert response.status_code == 200
        assert lastTask.name == response.get_json()['name']
        assert lastTask.id == response.get_json()['id']

def test_delete(app, client):
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.get('/tasks/delete/'+str(lastTask.id))
        assert response.status_code == 302

        task = operations.getById(lastTask.id)
        assert task is None
        #https://python.plainenglish.io/api-testing-with-pytest-71f213004e93