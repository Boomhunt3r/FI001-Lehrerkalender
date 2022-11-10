from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
import Server

auth = Blueprint('auth', __name__)

@auth.route('/index')
def login():
    return render_template('index.html')

@auth.route('/index', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Server.get_login_data(email)
    # user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user[2], password):
        flash('Bitte überprüfe deine Anmelde-Daten.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Server.get_login_data(email)

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    Server.set_login_data(email, generate_password_hash(password, method='sha256'))

    return redirect((url_for('auth.login')))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))