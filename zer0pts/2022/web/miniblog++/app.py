#!/usr/bin/env python
from Crypto.Cipher import AES
import base64
import datetime
import flask
import glob
import hashlib
import io
import json
import os
import re
import zipfile

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.encryption_key = os.urandom(16)

BASE_DIR = './post'
TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
  </head>
  <body>
    <h1>{{author}}'s Website</h1>
    <p>This is a sample page by {{author}} published on {{date}}.</p>
  </body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    db = get_database()
    if db is None:
        return flask.render_template('login.html')
    else:
        return flask.render_template('index.html',
                                     template=TEMPLATE, database=db)

@app.route('/post/<title>', methods=['GET'])
def get_post(title):
    db = get_database()
    if db is None:
        return flask.redirect('/login')

    err, post = db.read(title)
    if err:
        return flask.abort(404, err)

    return flask.render_template_string(post['content'],
                                        title=post['title'],
                                        author=post['author'],
                                        date=post['date'])

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['username'], str)
        assert isinstance(data['password'], str)
    except:
        return flask.abort(400, "Invalid request")

    flask.session['username'] = data['username']
    flask.session['passhash'] = hashlib.md5(data['password'].encode()).hexdigest()
    flask.session['workdir'] = os.urandom(16).hex()
    return flask.jsonify({'result': 'OK'})

@app.route('/api/new', methods=['POST'])
def api_new():
    """Add a blog post"""
    db = get_database()
    if db is None:
        return flask.redirect('/login')

    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['title'], str)
        assert isinstance(data['content'], str)
    except:
        return flask.abort(400, "Invalid request")

    err, post_id = db.add(data['title'], get_username(), data['content'])
    if err:
        return flask.jsonify({'result': 'NG', 'reason': err})
    else:
        return flask.jsonify({'result': 'OK', 'id': post_id})

@app.route('/api/delete', methods=['POST'])
def api_delete():
    """Delete a blog post"""
    db = get_database()
    if db is None:
        return flask.redirect('/login')

    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['id'], str)
    except:
        return flask.abort(400, "Invalid request")

    err = db.delete(data['id'])
    if err:
        return flask.jsonify({'result': 'NG', 'reason': err})
    else:
        return flask.jsonify({'result': 'OK'})

@app.route('/api/export', methods=['GET'])
def api_export():
    """Export blog posts"""
    db = get_database()
    if db is None:
        return flask.redirect('/login')

    err, blob = db.export_posts(get_username(), get_passhash())
    if err:
        return flask.jsonify({'result': 'NG', 'reason': err})
    else:
        return flask.jsonify({'result': 'OK', 'export': blob})

@app.route('/api/import', methods=['POST'])
def api_import():
    """Import blog posts"""
    db = get_database()
    if db is None:
        return flask.redirect('/login')

    try:
        data = json.loads(flask.request.data)
        assert isinstance(data['import'], str)
    except:
        return flask.abort(400, "Invalid request")

    err = db.import_posts(data['import'], get_username(), get_passhash())
    if err:
        return flask.jsonify({'result': 'NG', 'reason': err})
    else:
        return flask.jsonify({'result': 'OK'})

class Database(object):
    """Database to store blog posts of a user
    """
    def __init__(self, workdir):
        assert workdir.isalnum()
        self.workdir = f'{BASE_DIR}/{workdir}'
        os.makedirs(self.workdir, exist_ok=True)

    def __iter__(self):
        """Return blog posts sorted by publish date"""
        def enumerate_posts(workdir):
            posts = []
            for path in glob.glob(f'{workdir}/*.json'):
                with open(path, "r") as f:
                    posts.append(json.load(f))
            for post in sorted(posts,
                               key=lambda post: datetime.datetime.strptime(
                                   post['date'], "%Y/%m/%d %H:%M:%S"
                               ))[::-1]:
                yield post
        return enumerate_posts(self.workdir)

    @staticmethod
    def to_snake(s):
        """Convert string to snake case"""
        for i, c in enumerate(s):
            if not c.isalnum():
                s = s[:i] + '_' + s[i+1:]
        return s

    def add(self, title, author, content):
        """Add new blog post"""
        # Validate title and content
        if len(title) == 0: return 'Title is emptry', None
        if len(title) > 64: return 'Title is too long', None
        if len(content) == 0     : return 'HTML is empty', None
        if len(content) > 1024*64: return 'HTML is too long', None
        if '{%' in content:
            return 'The pattern "{%" is forbidden', None
        for brace in re.findall(r"{{.*?}}", content):
            if not re.match(r"{{!?[a-zA-Z0-9_]+}}", brace):
                return 'You can only use "{{title}}", "{{author}}", and "{{date}}"', None

        # Save the blog post
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        post_id = Database.to_snake(title)
        data = {
            'title': title,
            'id': post_id,
            'date': now,
            'author': author,
            'content': content
        }
        with open(f'{self.workdir}/{post_id}.json', "w") as f:
            json.dump(data, f)

        return None, post_id

    def read(self, title):
        """Load a blog post"""
        post_id = Database.to_snake(title)
        if not os.path.isfile(f'{self.workdir}/{post_id}.json'):
            return 'The blog post you are looking for does not exist', None

        with open(f'{self.workdir}/{post_id}.json', "r") as f:
            return None, json.load(f)

    def delete(self, title):
        """Delete a blog post"""
        post_id = Database.to_snake(title)
        if not os.path.isfile(f'{self.workdir}/{post_id}.json'):
            return 'The blog post you are trying to delete does not exist'
        os.unlink(f'{self.workdir}/{post_id}.json')

    def export_posts(self, username, passhash):
        """Export all blog posts with encryption and signature"""
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'a', zipfile.ZIP_DEFLATED) as z:
            # Archive blog posts
            for path in glob.glob(f'{self.workdir}/*.json'):
                z.write(path)
            # Add signature so that anyone else cannot import this backup
            z.comment = f'SIGNATURE:{username}:{passhash}'.encode()

        # Encrypt archive so that anyone else cannot read the contents
        buf.seek(0)
        iv = os.urandom(16)
        cipher = AES.new(app.encryption_key, AES.MODE_CFB, iv)
        encbuf = iv + cipher.encrypt(buf.read())
        return None, base64.b64encode(encbuf).decode()

    def import_posts(self, b64encbuf, username, passhash):
        """Import blog posts from backup file"""
        encbuf = base64.b64decode(b64encbuf)
        cipher = AES.new(app.encryption_key, AES.MODE_CFB, encbuf[:16])
        buf = io.BytesIO(cipher.decrypt(encbuf[16:]))

        try:
            with zipfile.ZipFile(buf, 'r', zipfile.ZIP_DEFLATED) as z:
                # Check signature
                if z.comment != f'SIGNATURE:{username}:{passhash}'.encode():
                    return 'This is not your database'
                # Extract archive
                z.extractall()
        except:
            return 'The database is broken'

        return None

def get_username():
    return flask.session['username'] if 'username' in flask.session else None
def get_passhash():
    return flask.session['passhash'] if 'passhash' in flask.session else None
def get_workdir():
    return flask.session['workdir'] if 'workdir' in flask.session else None
def get_database():
    if (get_username() and get_passhash() and get_workdir()) is None:
        return None
    return Database(get_workdir())

if __name__ == '__main__':
    app.run()
