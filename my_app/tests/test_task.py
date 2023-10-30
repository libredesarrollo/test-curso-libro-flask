
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
    
    
    
    # assert response.json() == {
    #     "message": "User created successfully"
    # }
# def test_index_page__logged_in(client):
#     with client:
#         formdata = {'username': 'testuser', 'password': 'testing', 'remember_me': False}
#         client.post('/auth/login', data=formdata)
#         assert current_user.username == 'testuser'