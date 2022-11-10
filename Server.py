from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user, LoginManager
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from api import databaseHandler
from api import datatime
from models import User

app = Flask(__name__)
app.config['SESSION_KEY'] = 'DergeheimegeheimKey'
app.config['DEBUG'] = True

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = databaseHandler.get_login_data(email)

    if not user or not check_password_hash(user[2], password):
        return redirect(url_for('index'))

    app.config['SECRET_KEY'] = 'login'

    login_user(create_user(user[1], user[2], user[4]))
    return redirect(url_for('sidebar'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = databaseHandler.get_login_data(email)

    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))

    databaseHandler.set_login_data(email, generate_password_hash(password, method='sha256'))

    return redirect((url_for('index')))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/sidebar')
def sidebar():
    return render_template('sideBar.html')

@app.route('/classtable')
def classtable():
    students = databaseHandler.get_all_students()
    print(students)
    return render_template('classTable.html', students=students)

@app.route('/classtable', methods=('GET', 'POST'))
def create_student():
    if request.method == 'POST':
        name = request.form['forename']
        surname = request.form['surname']
        postcode = request.form['postcode']
        street = request.form['street']
        housenumber = request.form['number']
        teacher = request.form['teacher']

        if not name or not surname or not postcode or not street or not housenumber or not teacher:
            return redirect(url_for('classtable'))
        else:
            databaseHandler.set_student(name,surname, 'FI001', teacher, postcode, street, housenumber)
            return redirect(url_for('classtable'))

    return render_template('classTable.html')

@app.route('/classlist')
def classlist():
    classes = databaseHandler.get_all_classes()
    return render_template('class.html', classes=classes)

@app.route('/classlist', methods=('GET', 'POST'))
def create_class():
    name = request.form['classname']
    teacher = request.form['teacher']

    return render_template('class.html')

def create_user(email, password, is_active):
    return User(email, password, is_active)

app.run()