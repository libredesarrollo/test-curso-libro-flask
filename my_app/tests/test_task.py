
import json

def test_create(app, client):
    # res = client.get('/task/create')
    # assert res.status_code == 200
    # expected = {'hello': 'world'}
    # assert expected == json.loads(res.get_data(as_text=True))

    payload = {
        "name": "andres",
        "category": 1
    }

    response =  client.post("/tasks/create", data=payload)

    # assert response.status_code == 200
    # assert response.json() == {
    #     "message": "User created successfully"
    # }
# def test_index_page__logged_in(client):
#     with client:
#         formdata = {'username': 'testuser', 'password': 'testing', 'remember_me': False}
#         client.post('/auth/login', data=formdata)
#         assert current_user.username == 'testuser'