
import logging
import click

from my_app import app,db
from my_app.auth.models import User

def register(app):
    @app.cli.command('create-user')
    @click.argument('username')
    @click.argument('password')
    def create_user(username, password):

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            click.echo( 'This username has been already taken. Try another one.')
        
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        click.echo('User {0} Added.'.format(username))

    @app.cli.command('mycmd')
    def mycmd():
        click.echo("Test")

    @app.shell_context_processor
    def myctx():
        return {'myvar': 'value'}