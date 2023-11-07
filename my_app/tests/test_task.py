
import json

from my_app.tasks import operations

def test_create(app, client):
    response = client.get('/tasks/create')

    assert response.status_code == 200
    assert b'<input id="name" name="name" required type="text" value="">' in response.get_data()
    assert '<input id="name" name="name" required type="text" value="">' in response.get_data(as_text=True)

    dataform = {
        "name": "andres",
        "category": 1
    }

    tasksCount=0
    with app.app_context():
        tasksCount = len(operations.getAll())
    response =  client.post("/tasks/create", data=dataform)

    assert response.status_code == 200
    assert '<input id="name" name="name" required type="text" value="'+dataform.get('name')+'">' in response.get_data(as_text=True)
    with app.app_context():
        assert len(operations.getAll()) == tasksCount+1
        lastTask = operations.getLastTask()
        assert lastTask.name == dataform.get('name') and lastTask.category_id == dataform.get('category')


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

def test_index(app, client):
    with app.app_context():
        response = client.get('/tasks/')
        assert response.status_code == 200
        tasks = operations.getAll()
        for t in tasks:
            assert '<td>'+t.name+'</td>' in response.get_data(as_text=True)

def test_delete(app, client):
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.get('/tasks/delete/'+str(lastTask.id))
        assert response.status_code == 302

        task = operations.getById(lastTask.id)
        assert task is None