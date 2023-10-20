from flask_restful import Resource, reqparse
from flask import g

class UserApi(Resource): 
# @app.route('/api/login')
# @auth.login_required

    def get(self):
        token = g.user.generate_auth_token(600)
        return { 'token': token.decode('ascii'), 'duration': 600 }