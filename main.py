from flask import Blueprint, render_template
from flask_login import login_required, current_user
import Server

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    Server.index()