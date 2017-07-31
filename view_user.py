from app import lm, bcrypt
from models import User
from forms import LoginForm
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user


vu = Blueprint('user', __name__)


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
