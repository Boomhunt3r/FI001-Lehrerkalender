import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('lehrerkalender.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET KEY'] = 'Der geheime geheim Key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts(title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

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
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def get_login_data(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Login WHERE Email = ?',
                        (email,)).fetchone()


    return user

def get_classes():
    conn = get_db_connection()
    classes = conn.execute('SELECT * FROM Klasse ').fetchall()
    conn.close()
    return classes

def get_class(id):
    conn = get_db_connection()

    return None

def get_students_in_class(id):
    conn = get_db_connection()

    return None

def get_student(id):
    conn = get_db_connection()

    return None

def get_appointments(id):
    conn = get_db_connection()

    return None

def get_appointment(id):
    conn = get_db_connection()

    return None

def set_student(id):
    conn = get_db_connection()

    return None

def set_class(id):
    conn = get_db_connection()

    return None

def set_appointment(id):
    conn = get_db_connection()

    return None

def set_login_data(id):
    conn = get_db_connection()

    return None


print(get_login_data('laqua@gso.schule.koeln'))

#app.run()