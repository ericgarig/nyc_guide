from app import bcrypt, lm

from flask import Blueprint, jsonify, redirect, render_template, url_for

from flask_login import login_required, login_user, logout_user

from forms import LoginForm

from models import User, UserSchema


vu = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@lm.user_loader
def user_loader(id):
    return User.query.get(id)


@vu.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('welcome'))
    return render_template('login.html', form=form)


@vu.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))


@vu.route('/json/')
def json_list():
    return jsonify(user_schema.dump(User.query.all()).data)
