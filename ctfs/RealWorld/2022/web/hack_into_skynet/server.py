#!/usr/bin/env python3

import flask
import psycopg2
import datetime
import hashlib
from skynet import Skynet

app = flask.Flask(__name__, static_url_path='')
skynet = Skynet()

def skynet_detect():
    req = {
        'method': flask.request.method,
        'path': flask.request.full_path,
        'host': flask.request.headers.get('host'),
        'content_type': flask.request.headers.get('content-type'),
        'useragent': flask.request.headers.get('user-agent'),
        'referer': flask.request.headers.get('referer'),
        'cookie': flask.request.headers.get('cookie'),
        'body': str(flask.request.get_data()),
    }
    _, result = skynet.classify(req)
    return result and result['attack']

@app.route('/static/<path:path>')
def static_files(path):
    return flask.send_from_directory('static', path)

@app.route('/', methods=['GET', 'POST'])
def do_query():
    if skynet_detect():
        return flask.abort(403)

    if not query_login_state():
        response = flask.make_response('No login, redirecting', 302)
        response.location = flask.escape('/login')
        return response

    if flask.request.method == 'GET':
        return flask.send_from_directory('', 'index.html')
    elif flask.request.method == 'POST':
        kt = query_kill_time()
        if kt:
            result = kt 
        else:
            result = ''
        return flask.render_template('index.html', result=result)
    else:
        return flask.abort(400)

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if skynet_detect():
        return flask.abort(403)

    if flask.request.method == 'GET':
        return flask.send_from_directory('static', 'login.html')
    elif flask.request.method == 'POST':
        if not query_login_attempt():
            return flask.send_from_directory('static', 'login.html')
        else:
            session = create_session()
            response = flask.make_response('Login success', 302)
            response.set_cookie('SessionId', session)
            response.location = flask.escape('/')
            return response
    else:
        return flask.abort(400)

def query_login_state():
    sid = flask.request.cookies.get('SessionId', '')
    if not sid:
        return False

    now = datetime.datetime.now()
    with psycopg2.connect(
            host="challenge-db",
            database="ctf",
            user="ctf",
            password="ctf") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sessionid"
           "  FROM login_session"
           "  WHERE sessionid = %s"
           "    AND valid_since <= %s"
           "    AND valid_until >= %s"
           "", (sid, now, now))
        data = [r for r in cursor.fetchall()]
        return bool(data)

def query_login_attempt():
    username = flask.request.form.get('username', '')
    password = flask.request.form.get('password', '')
    if not username and not password:
        return False

    sql = ("SELECT id, account"
           "  FROM target_credentials"
           "  WHERE password = '{}'").format(hashlib.md5(password.encode()).hexdigest())
    user = sql_exec(sql)
    name = user[0][1] if user and user[0] and user[0][1] else ''
    return name == username

def create_session():
    valid_since = datetime.datetime.now()
    valid_until = datetime.datetime.now() + datetime.timedelta(days=1)
    sessionid = hashlib.md5((str(valid_since)+str(valid_until)+str(datetime.datetime.now())).encode()).hexdigest()

    sql_exec_update(("INSERT INTO login_session (sessionid, valid_since, valid_until)"
           "  VALUES ('{}', '{}', '{}')").format(sessionid, valid_since, valid_until))
    return sessionid

def query_kill_time():
    name = flask.request.form.get('name', '')
    if not name:
        return None

    sql = ("SELECT name, born"
           "  FROM target"
           "  WHERE age > 0"
           "    AND name = '{}'").format(name)
    nb = sql_exec(sql)
    if not nb:
        return None
    return '{}: {}'.format(*nb[0])

def sql_exec(stmt):
    data = list()
    try:
        with psycopg2.connect(
                host="challenge-db",
                database="ctf",
                user="ctf",
                password="ctf") as conn:
            cursor = conn.cursor()
            cursor.execute(stmt)
            for row in cursor.fetchall():
                data.append([col for col in row])
            cursor.close()
    except Exception as e:
        print(e)
    return data

def sql_exec_update(stmt):
    data = list()
    try:
        with psycopg2.connect(
                host="challenge-db",
                database="ctf",
                user="ctf",
                password="ctf") as conn:
            cursor = conn.cursor()
            cursor.execute(stmt)
            conn.commit()
    except Exception as e:
        print(e)
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
