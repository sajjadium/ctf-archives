import io
import ipaddress
import os
import socket
import ssl
from functools import wraps
from zipfile import ZipFile

import dns.resolver
import gevent
import sqlalchemy.exc
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Util.number import bytes_to_long, ceil_div, long_to_bytes, size
from OpenSSL import crypto
from flask import Flask, flash, redirect, render_template, request, send_file, session
from flask_sqlalchemy import SQLAlchemy
from gunicorn.workers.ggevent import GeventWorker
from validator_collection import checkers
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


class TimeoutWorker(GeventWorker):
    def handle_request(self, listener_name, req, sock, addr):
        with gevent.Timeout(10):
            super().handle_request(listener_name, req, sock, addr)


app.debug = 'DEBUG' in os.environ

with open('secret', 'rb') as f:
    app.config['SECRET_KEY'] = f.read()

if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:cybercyber@database/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

db = SQLAlchemy(app)


### DB ###


class User(db.Model):
    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    n = db.Column(db.Text, nullable=True)
    e = db.Column(db.String(1000), nullable=True)
    challenge = db.Column(db.String(64), nullable=True)
    domain = db.Column(db.String(100), nullable=True)

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)


### Endpoints ####
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return f(*args, **kwargs)
        else:
            flash('You have to allowed to perform this action', 'danger')
            return redirect('/login')

    return wrap


@app.route('/')
def index():
    if 'name' in session:
        return redirect('/home')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    name = request.form.get('name', '')
    password = request.form.get('password', '')

    if user := User.query.filter_by(name=name).first():
        if check_password_hash(user.password, password):
            session['name'] = user.name
            return redirect('/home')

    flash('Invalid credentials', 'danger')
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form.get('name', '')
    password = request.form.get('password', '')

    try:
        user = User(name, password)
        db.session.add(user)

        db.session.commit()

        session['name'] = user.name
    except sqlalchemy.exc.DBAPIError:
        db.session.rollback()
        db.session.flush()

        flash('Username already taken', 'danger')
        return redirect('/register')

    return redirect('/home')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/home')
@is_logged_in
def home():
    return render_template('home.html')


@app.route('/set_pubkey', methods=['GET', 'POST'])
@is_logged_in
def set_pubkey():
    if request.method == 'GET':
        return render_template('set_pubkey.html')

    try:
        n = int(request.form.get('n'))
        if n < 2 ** 1024:
            raise ValueError
        e = int(request.form.get('e'))
        if e < 0:
            raise ValueError

        RSA.RsaKey(n=n, e=e)
    except ValueError:
        flash('This does not look like a valid RSA key', 'danger')
        return render_template('set_pubkey.html')

    try:
        if user := User.query.filter_by(name=session['name']).first():
            user.n = f'{n:x}'
            user.e = f'{e:x}'
            db.session.commit()

            flash('Successfully added public key', 'success')
            return redirect('/home')
    except sqlalchemy.exc.DBAPIError:
        db.session.rollback()
        db.session.flush()

        flash('Something went wrong', 'danger')
        return redirect('/set_pubkey')


@app.route('/request_challenge', methods=['GET', 'POST'])
@is_logged_in
def request_challenge():
    user = User.query.filter_by(name=session['name']).first()

    if not (user.n and user.e):
        flash('Please set a public key first', 'danger')
        return redirect('/home')

    if request.method == 'GET':
        return render_template('ask_domain.html')

    domain = request.form.get('domain', '')
    if not checkers.is_domain(domain):
        flash('This does not look like a domain', 'danger')
        return render_template('ask_domain.html')

    try:
        user.challenge = os.urandom(32).hex()
        user.domain = domain
        db.session.commit()
    except sqlalchemy.exc.DBAPIError:
        db.session.rollback()
        db.session.flush()

        flash('Something went wrong', 'danger')
        return redirect('/home')

    return render_template('request_challenge.html', user=user)


@app.route('/get_certificate')
@is_logged_in
def get_certificate():
    user = User.query.filter_by(name=session['name']).first()

    try:
        public_key = RSA.RsaKey(n=int(user.n, 16), e=int(user.e, 16))

        signature = bytes.fromhex(str(dns.resolver.resolve(f'_acme.{user.domain}', 'TXT')[0]).replace('"', '').replace(' ', '').strip())
        signature = long_to_bytes(bytes_to_long(signature) % public_key.n).rjust(ceil_div(size(public_key.n), 8), b'\x00')

        h = SHA256.new(bytes.fromhex(user.challenge))
        verifier = pkcs1_15.new(public_key)

        verifier.verify(h, signature)

        with open('ca.crt', 'rb') as f:
            cacert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        cert = crypto.X509()
        cert.get_subject().C = "DE"
        cert.get_subject().ST = "NRW"
        cert.get_subject().O = "RedRocket"
        cert.get_subject().OU = "Applied Cyberforces"
        cert.get_subject().CN = user.domain
        cert.get_subject().emailAddress = "lol@lol.lol"
        cert.set_issuer(cacert.get_subject())
        cert.set_serial_number(1337)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_pubkey(k)

        with open('ca.key', 'rb') as f:
            cakey = crypto.load_privatekey(buffer=f.read(), type=crypto.FILETYPE_PEM)

        cert.sign(cakey, 'sha512')

        cert_chain = crypto.dump_certificate(crypto.FILETYPE_PEM, cert) + crypto.dump_certificate(crypto.FILETYPE_PEM, cacert)

        stream = io.BytesIO()
        with ZipFile(stream, 'w') as zf:
            zf.writestr('server.crt',  cert_chain, compress_type=None)
            zf.writestr('server.key', crypto.dump_privatekey(crypto.FILETYPE_PEM, k), compress_type=None)
        stream.seek(0)

        user.challenge = None
        db.session.commit()

        return send_file(
            stream,
            as_attachment=True,
            download_name='certificates.zip'
        )
    except ValueError:
        flash('The signature is invalid', 'danger')
    except dns.resolver.NoAnswer:
        flash('DNS response is empty', 'danger')
    except gevent.Timeout:
        flash('Timeout exceeded', 'danger')
    except:
        flash('Something went wrong', 'danger')

    db.session.rollback()
    db.session.flush()
    return redirect('/home')


@app.route('/request_flag', methods=['GET', 'POST'])
@is_logged_in
def request_flag():
    if request.method == 'GET':
        return render_template('request_flag.html')

    ip = request.form.get('ip', '')
    if not checkers.is_ipv4(ip):
        flash('This does not look like an IPv4 address', 'danger')
        return render_template('request_flag.html')

    # Make sure to only send the flag to the ctf organizers
    hostname = 'rumble.host'
    context = ssl.create_default_context(cafile='ca.crt')

    try:
        if ipaddress.ip_address(ip).is_private and not app.debug:
            raise ValueError

        with socket.create_connection((ip, 1337)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.sendall(os.environ['FLAG'].encode())

        flash('Flag send successfully', 'success')
    except ssl.SSLCertVerificationError:
        flash('TLS Handshake failed', 'danger')
    except ConnectionRefusedError:
        flash('Connection got refused', 'danger')
    except gevent.Timeout:
        flash('Timeout exceeded', 'danger')
    except:
        flash('Something went wrong while sending the flag', 'danger')
    return redirect('/home')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(threaded=True)
