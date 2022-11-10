from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user, LoginManager
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from api import databaseHandler
from api import datatime
from models import User

app = Flask(__name__)
app.config['SESSION_KEY'] = 'DergeheimegeheimKey'
#app.config['SESSION_TYPE'] = 'redis'
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
        #app.config['SECRET_KEY'] = 'nologin'
        return redirect(url_for('index'))

    app.config['SECRET_KEY'] = 'login'

    login_user(user)
    return redirect(url_for('dashboard'))

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    students = databaseHandler.get_all_students()
    print(students)
    return render_template('classTable.html', students=students)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('classTable.html', classes=post)

@app.route('/dashboard', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['forename']
        surname = request.form['surname']
        postcode = request.form['postcode']
        street = request.form['street']
        housenumber = request.form['number']
        teacher = request.form['teacher']

        if not name:
            flash('Bitte geben sie einen Namen an.')
        else:
            databaseHandler.set_student(name,surname, 'FI001', teacher, postcode, street, housenumber)
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         'WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

app.run()