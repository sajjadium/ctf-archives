import base64
import flask
from flask_wtf.csrf import CSRFProtect
import hashlib
import json
import os
import re
import redis
import requests

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
RECAPTCHA_KEY = os.getenv('RECAPTCHA_KEY', '')
SALT = os.getenv('SALT', os.urandom(8))

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
csrf = CSRFProtect(app)

"""
Utility functions
"""
def login_ok():
    """Check if the current user is logged in"""
    return 'user' in flask.session

def conn_user():
    """Create a connection to user database"""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
def conn_report():
    """Create a connection to report database"""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)

def success(message):
    """Return a success message"""
    return flask.jsonify({'status': 'success', 'message': message})
def error(message):
    """Return an error message"""
    return flask.jsonify({'status': 'error', 'message': message})

def passhash(password):
    """Get a safe hash value of password"""
    return hashlib.sha256(SALT + password.encode()).hexdigest()

"""
Enforce CSP
"""
@app.after_request
def after_request(response):
    csp  = ""
    csp +=  "default-src 'none';"
    if 'csp_nonce' in flask.g:
        csp += f"script-src 'nonce-{flask.g.csp_nonce}' https://cdn.jsdelivr.net/ https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/ 'unsafe-eval';"
    else:
        csp += f"script-src https://cdn.jsdelivr.net/ https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/ 'unsafe-eval';"
    csp += f"style-src https://cdn.jsdelivr.net/;"
    csp += f"frame-src https://www.google.com/recaptcha/ https://recaptcha.google.com/recaptcha/;"
    csp += f"base-uri 'none';"
    csp += f"connect-src 'self';"
    response.headers['Content-Security-Policy'] = csp
    return response

@app.context_processor
def csp_nonce_init():
    flask.g.csp_nonce = base64.b64encode(os.urandom(16)).decode()
    return dict(csp_nonce=flask.g.csp_nonce)

"""
Route
"""
@app.route('/')
def home():
    if login_ok():
        conn = conn_user()
        bio = conn.hget(flask.session['user'], 'bio').decode()
        if bio is not None:
            return flask.render_template('index.html',
                                         username=flask.session['user'], bio=bio)
    return flask.render_template('login.html')

@app.route('/profile/<user>')
def profile(user):
    if not login_ok():
        return flask.redirect(flask.url_for('home'))

    is_report = flask.request.args.get('report') is not None

    conn = conn_user()
    if not conn.exists(user):
        return flask.redirect(flask.url_for('home'))

    bio = conn.hget(user, 'bio').decode()
    return flask.render_template('profile.html',
                                 username=user, bio=bio,
                                 is_report=is_report)

"""
User API
"""
@app.route('/api/user/register', methods=['POST'])
def user_register():
    """Register a new user"""
    # Check username and password
    username = flask.request.form.get('username', '')
    password = flask.request.form.get('password', '')
    if re.match("^[-a-zA-Z0-9_]{5,20}$", username) is None:
        return error("Username must follow regex '^[-a-zA-Z0-9_]{5,20}$'")
    if re.match("^.{8,128}$", password) is None:
        return error("Password must follow regex '^.{8,128}$'")

    # Register a new user
    conn = conn_user()
    if conn.exists(username):
        return error("This username has been already taken.")
    else:
        conn.hset(username, mapping={
            'password': passhash(password),
            'bio': "<p>Hello! I'm new to this website.</p>"
        })
        flask.session['user'] = username
        return success("Successfully registered a new user.")

@app.route('/api/user/login', methods=['POST'])
def user_login():
    """Login user"""
    if login_ok():
        return success("You have already been logged in.")

    username = flask.request.form.get('username', '')
    password = flask.request.form.get('password', '')

    # Check password
    conn = conn_user()
    if conn.hget(username, 'password').decode() == passhash(password):
        flask.session['user'] = username
        return success("Successfully logged in.")
    else:
        return error("Invalid password or user does not exist.")

@app.route('/api/user/logout', methods=['POST'])
def user_logout():
    """Logout user"""
    if login_ok():
        flask.session.clear()
        return success("Successfully logged out.")
    else:
        return error("You are not logged in.")

@app.route('/api/user/update', methods=['POST'])
def user_update():
    """Update user info"""
    if not login_ok():
        return error("You are not logged in.")

    username = flask.session['user']
    bio = flask.request.form.get('bio', '')
    if len(bio) > 2000:
        return error("Bio is too long.")

    # Update bio
    conn = conn_user()
    conn.hset(username, 'bio', bio)

    return success("Successfully updated your profile.")

"""
Report spam account
"""
@app.route('/api/support/report', methods=['POST'])
def report():
    """Report spam
    Support staff will check the reported contents as soon as possible.
    """
    if RECAPTCHA_KEY:
        recaptcha = flask.request.form.get('recaptcha', '')
        params = {
            'secret': RECAPTCHA_KEY,
            'response': recaptcha
        }
        r = requests.get(
            "https://www.google.com/recaptcha/api/siteverify", params=params
        )
        if json.loads(r.text)['success'] == False:
            abort(400)

    username = flask.request.form.get('username', '')
    conn = conn_user()
    if not conn.exists(username):
        return error("This user does not exist.")

    conn = conn_report()
    conn.rpush('report', username)
    return success("""Thank you for your report.<br>Our support team will check the post as soon as possible.""")


if __name__ == '__main__':
    app.run()
