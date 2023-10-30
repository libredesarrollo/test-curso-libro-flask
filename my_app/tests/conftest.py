# import pytest
# from my_app import app

# @pytest.fixture()
# def app():
#     app.config.update({
#         "TESTING": True,
#     })

#     # other setup can go here

#     yield app

#     # clean up / reset resources here


# @pytest.fixture()
# def client(app):
#     return app.test_client()


# # @pytest.fixture()
# # def runner(app):
# #     return app.test_cli_runner()

# def test_request_example(client):
#     response = client.get("/posts")
#     assert b"<h2>Hello, World!</h2>" in response.data


import pytest
from my_app.config import TestingConfig
from my_app import app as flask_app

@pytest.fixture
def app():
    yield flask_app
    
@pytest.fixture
def client(app):
    app.config.from_object(TestingConfig) 
    # app.config.update({
    #     "TESTING": True,
    # })
    # app.config['WTF_CSRF_ENABLED'] = False
    return app.test_client()