import os
import bcrypt
import db
import forms

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, request, session, redirect

path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.template_folder = os.path.join(path, 'templates')
app.static_folder = os.path.join(path, 'static')

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/tasks')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    form = forms.AccountForm(request.form)

    if not form.validate():
        return render_template('error.html', message='Invalid login'), 400

    username = form.username.data.lower()

    if not db.has(username):
        return render_template('error.html', message='Invalid login'), 400

    user = db.get(username)
    
    if not bcrypt.checkpw(form.password.data.encode(), user['password'].encode()):
        return render_template('error.html', message='Invalid login'), 400

    session['username'] = username

    return redirect('/tasks')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form = forms.AccountForm(request.form)

        if not form.validate():
            return render_template('error.html', message='Invalid registration'), 400

        username, password = form.username.data.lower(), form.password.data

        if db.has(username):
            return render_template('error.html', message='User already exists!'), 400


        db.put(username, {
            'tasks': [],
            'password': bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
        })

        session['username'] = username

        return redirect('/tasks')

@app.route('/tasks')
def tasks():
    if 'username' not in session:
        return redirect('/')

    tasks = db.get(session['username'])['tasks']

    if 'search' in request.args:
        search = request.args['search']
        tasks = list(filter(lambda task: search in task['content'], tasks))

    tasks = list(sorted(tasks, key=lambda task: -task['priority']))

    return render_template('tasks.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        form = forms.TaskForm(request.form)

        if not form.validate():
            return render_template('error.html', message='Invalid task'), 400

        user = db.get(session['username'])

        if len(user['tasks']) >= 5:
            return render_template('error.html', message='Maximum task limit reached!'), 400

        task = {
            'title': form.title.data,
            'content': form.content.data,
            'priority': form.priority.data,
            'id': len(user['tasks'])
        }

        user['tasks'].append(task)

        db.put(session['username'], user)

        return redirect('/tasks')

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if 'username' not in session:
        return redirect('/')

    try:
        task_id = int(task_id)
    except:
        return render_template('error.html', message='Invalid task'), 400

    user = db.get(session['username'])
    task = next((task for task in user['tasks'] if task['id'] == task_id), None)

    if task is None:
        return render_template('error.html', message='Task not found'), 404

    if request.method == 'GET':
        return render_template('edit.html', id=task['id'])
    elif request.method == 'POST':
        form = forms.EditForm(request.form)

        if not form.validate():
            return render_template('error.html', message='Invalid edit'), 400

        for attribute in ['title', 'content', 'priority']:
            if form[attribute].data:
                task[attribute] = form[attribute].data

        db.put(session['username'], user)

        return redirect('/tasks')
