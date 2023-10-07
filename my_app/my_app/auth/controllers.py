from flask import g, redirect, url_for, render_template, flash, Blueprint 
from flask_login import current_user, login_user, logout_user, login_required

from my_app import login_manager
from my_app.auth.models import User 
from my_app.auth.forms import  RegistrationForm, LoginForm 

authRoute = Blueprint('auth', __name__) 
 
@login_manager.user_loader 
def load_user(id): 
    return User.query.get(int(id)) 
 
@authRoute.before_request 
def get_current_user(): 
    g.user = current_user

@authRoute.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('auth.home'))

    form = LoginForm()

    if form.validate_on_submit():
        # username = request.form.get('username')
        # password = request.form.get('password')
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)

        login_user(existing_user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)
 
@authRoute.route('/logout') 
@login_required 
def logout(): 
    logout_user() 
    return redirect(url_for('home')) 