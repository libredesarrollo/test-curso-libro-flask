from flask import g, redirect, url_for, render_template, flash, Blueprint, request, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_jwt_extended import create_access_token

from my_app import login_manager, db
from my_app.auth.helpers import authenticate
from my_app.auth.models import User
from my_app.auth.forms import  RegistrationForm, LoginForm

authRoute = Blueprint('auth', __name__) 
 
@login_manager.user_loader 
def load_user(id): 
    return User.query.get(int(id))


# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try token
#     user = User.verify_auth_token(username_or_token)
#     # then check for username and password pair
#     if not user:
#         user = User.query.filter_by(username = username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#         g.user = user
#     return True
 
@authRoute.before_request 
def get_current_user(): 
    g.user = current_user

@authRoute.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('tasks.index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('user/login.html', form=form)

        login_user(existing_user)
        session['user'] = existing_user.serialize
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('tasks.index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('user/login.html', form=form)

@authRoute.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Your are already logged in.', 'info')
        return redirect(url_for('tasks.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # username = request.form.get('username')
        # password = request.form.get('password')
        username = form.username.data
        password = form.password.data
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash(
                'This username has been already taken. Try another one.',
                'warning'
            )
            return render_template('user/register.html', form=form)
        
        user = User(username, password)
        db.session.add(user)
        db.session.commit()

        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('user.login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('user/register.html', form=form)

@authRoute.route('/user/api', methods=['POST'])
def api():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@authRoute.route('/logout') 
@login_required 
def logout(): 
    logout_user() 
    return redirect(url_for('auth.login')) 


#Profile
@authRoute.route('/<int:id>')
def profile():
   
   return render_template('user/profile.html')
