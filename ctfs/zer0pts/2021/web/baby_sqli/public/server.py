import flask
import os
import re
import hashlib
import subprocess

app = flask.Flask(__name__)
app.secret_key = os.urandom(32)

def sqlite3_query(sql):
    p = subprocess.Popen(['sqlite3', 'database.db'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    o, e = p.communicate(sql.encode())
    if e:
        raise Exception(e)
    result = []
    for row in o.decode().split('\n'):
        if row == '': break
        result.append(tuple(row.split('|')))
    return result

def sqlite3_escape(s):
    return re.sub(r'([^_\.\sa-zA-Z0-9])', r'\\\1', s)

@app.route('/')
def home():
    msg = ''
    if 'msg' in flask.session:
        msg = flask.session['msg']
        del flask.session['msg']
    if 'name' in flask.session:
        return flask.render_template('index.html', name=flask.session['name'])
    else:
        return flask.render_template('login.html', msg=msg)

@app.route('/login', methods=['post'])
def auth():
    username = flask.request.form.get('username', default='', type=str)
    password = flask.request.form.get('password', default='', type=str)
    if len(username) > 32 or len(password) > 32:
        flask.session['msg'] = 'Too long username or password'
        return flask.redirect(flask.url_for('home'))

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    result = None
    try:
        result = sqlite3_query(
            'SELECT * FROM users WHERE username="{}" AND password="{}";'
            .format(sqlite3_escape(username), password_hash)
        )
    except:
        pass

    if result:
        flask.session['name'] = username
    else:
        flask.session['msg'] = 'Invalid Credential'
    return flask.redirect(flask.url_for('home'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8888,
        debug=False,
        threaded=True
    )
