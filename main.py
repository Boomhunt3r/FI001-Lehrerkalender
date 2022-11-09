from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from . import Server

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    Server.index()

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)