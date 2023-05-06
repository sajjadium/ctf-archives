import datetime as dt
import hashlib
import os
import random
import secrets

import aioredis
import quart
import quart_rate_limiter
from quart_rate_limiter.redis_store import RedisStore
import requests

SECRET_KEY   = os.environ['SECRET_KEY']
REDIS_HOST   = os.environ['REDIS_HOST']

redis = aioredis.from_url(f"redis://{REDIS_HOST}")

app = quart.Quart(__name__)
redis_store = RedisStore(f"redis://{REDIS_HOST}")
limiter = quart_rate_limiter.RateLimiter(app, store=redis_store)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

def password_hash(password: str, *, salt: bytes=None) -> str:
    salt = salt or random.randbytes(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    return f"{salt.hex()}:{hashed.hex()}"

def password_verify(password: str, hashed: str) -> bool:
    try:
        salt, hash_ = map(bytes.fromhex, hashed.split(':'))
    except ValueError:
        return False
    
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000) == hash_

async def login(username: str, password: str) -> bool:
    password_hash = await redis.get(f'user:{username}')
    if password_hash is None:
        return False
    
    return password_verify(password, password_hash.decode())

async def register(username: str, password: str) -> bool:
    # race condition but :shrug:
    if await redis.get(f'user:{username}'):
        return False
    
    await redis.set(f'user:{username}', password_hash(password))
    return True

async def get_user_note(username: str) -> str:
    note = await redis.get(f'note:{username}')
    return '' if note is None else note.decode()

async def set_user_note(username: str, note: str):
    await redis.set(f'note:{username}', note)

@app.before_serving
async def startup():
    print('Notepad starting...')
    # We don't care if this fails, we just want to reserve the admin username so no one gets confused
    await register('admin', secrets.token_hex(24))

@app.after_request
async def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
    resp.headers['X-Frame-Options'] = 'none'
    return resp

@app.errorhandler(404)
async def not_found(e):
    return "404 Not Found", 404

@app.route('/')
async def index():
    return await quart.render_template('index.html')

@app.route('/robots.txt')
async def robots():
    return "Disallow:\n/admin\n/me", 200, {'Content-Type': 'text/plain'}

@app.route('/login', methods=['GET', 'POST'])
async def login_():
    err = ''
    if quart.request.method == "POST":
        form = await quart.request.form
        username, password = map(form.get, ['username', 'password'])

        if username is None or password is None:
            err = "Username and password must be specified"
        elif not await login(username, password):
            err = "Invalid username or password"
        else:
            quart.session['user'] = username
            return quart.redirect(quart.url_for('me'))
    
    return await quart.render_template('login.html', err=err)

@app.route('/register', methods=['GET', 'POST'])
async def register_():
    err = ''
    if quart.request.method == "POST":
        form = await quart.request.form
        username, password = map(form.get, ['username', 'password'])

        if username is None or password is None:
            err = "Username and password must be specified"
        elif not await register(username, password):
            err = "Username already in-use"
        else:
            return quart.redirect(quart.url_for('login_'))
    
    
    return await quart.render_template('register.html', err=err)

@app.route('/logout')
async def logout_():
    quart.session.clear()
    return quart.redirect(quart.url_for('index'))

@app.route('/me', methods=['GET', 'POST'])
async def me():
    user = quart.session.get('user')
    if not user:
        return quart.redirect(quart.url_for('index'))

    err = ''
    if quart.request.method == 'POST':
        form = await quart.request.json
        note = form.get('note', '')

        await set_user_note(user, note)
    else:
        note = await get_user_note(user)

    return await quart.render_template('me.html', note=note, username=user)

@app.route('/admin')
async def admin():
    if quart.session.get('admin') != 1:
        return "", 403
    return open('flag.txt').read()

@app.route('/report', methods=["GET", "POST"])
@quart_rate_limiter.rate_limit(5, dt.timedelta(seconds=10))
async def report():
    user = quart.session.get('user')
    if not user:
        return quart.redirect(quart.url_for('index'))
    if quart.session.get('admin') == 1:
        # Just in case anyone tries it
        return "You're the admin... Go fix it yourself", 418

    if quart.request.method == 'POST':
        form = await quart.request.form
        url = form.get('url')
        if url:
            __stub_get_url(url)
            return quart.redirect(quart.url_for('me'))

    return await quart.render_template('report.html')

@app.route('/__stub/admin/login')
async def __stub_admin_login():
    quart.session['admin'] = 1
    return "Ok"
