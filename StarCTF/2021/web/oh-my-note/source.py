import string
import random
import time
import datetime
from flask import render_template, redirect, url_for, request, session, Flask
from functools import wraps
from exts import db
from config import Config
from models import User, Note
from forms import CreateNoteForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not session.get("username"):
               return redirect(url_for('index'))
            return f(*args, **kws)
    return decorated_function


def get_random_id():
    alphabet = list(string.ascii_lowercase + string.digits)
    return ''.join([random.choice(alphabet) for _ in range(32)])


@app.route('/')
@app.route('/index')
def index():
    results = Note.query.filter_by(prv='False').limit(100).all()
    notes = []
    for x in results:
        note = {}
        note['title'] = x.title
        note['note_id'] = x.note_id
        notes.append(note)

    return render_template('index.html', notes=notes)


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    try:
        form = CreateNoteForm()
        if request.method == "POST":
            username = form.username.data
            title = form.title.data
            text = form.body.data
            prv = str(form.private.data)
            user = User.query.filter_by(username=username).first()

            if user:
                user_id = user.user_id
            else:
                timestamp = round(time.time(), 4)
                random.seed(timestamp)
                user_id = get_random_id()
                user = User(username=username, user_id=user_id)
                db.session.add(user)
                db.session.commit()
                session['username'] = username

            timestamp = round(time.time(), 4)

            post_at = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

            random.seed(user_id + post_at)
            note_id = get_random_id()

            note = Note(user_id=user_id, note_id=note_id,
                        title=title, text=text,
                        prv=prv, post_at=post_at)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('index'))

        else:
            return render_template("create.html", form=form)
    except Exception as e:
        pass


@app.route('/my_notes')
def my_notes():
    if session.get('username'):
        username = session['username']
        user_id = User.query.filter_by(username=username).first().user_id
    else:
        user_id = request.args.get('user_id')
        if not user_id:
            return redirect(url_for('index'))

    results = Note.query.filter_by(user_id=user_id).limit(100).all()
    notes = []
    for x in results:
        note = {}
        note['title'] = x.title
        note['note_id'] = x.note_id
        notes.append(note)

    return render_template("my_notes.html", notes=notes)


@app.route('/view/<_id>')
def view(_id):
    note = Note.query.filter_by(note_id=_id).first()
    user_id = note.user_id
    username = User.query.filter_by(user_id=user_id).first().username
    data = {
        'post_at': note.post_at,
        'title': note.title,
        'text': note.text,
        'username': username
    }

    return render_template('note.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)