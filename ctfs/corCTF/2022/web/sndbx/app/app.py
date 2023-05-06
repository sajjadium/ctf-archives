import secrets
import config
import signer
import manager

from flask import Flask, session, render_template, request
from flask_session import Session
from cryptography.hazmat.primitives import serialization
from cryptography import x509

app = Flask(__name__)
app.config.from_object(config)

Session(app)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/ca')
def ca():
	return signer.ca_pem, 200, { 'Content-Type': 'text/plain' }

@app.route('/', subdomain='<subdomain>')
def user(subdomain):
	with open(f'content/{subdomain}', 'rb') as f:
		return f.read().decode(encoding='UTF-8'), 200, { 'Content-Type': 'text/html' }

@app.route('/create', methods=['POST'])
def create():
	if 'subdomain' in session:
		return render_template('error.html', error='Already have a subdomain!'), 400

	subdomain = secrets.token_urlsafe(16).lower()

	session['csr-subdomain'] = subdomain

	return render_template('csr.html', subdomain=subdomain)

@app.route('/add', methods=['POST'])
def add():
	if 'csr-subdomain' not in session:
		return render_template('error.html', error='Subdomain not found!'), 400

	if 'csr' not in request.form or 'priv' not in request.form:
		return render_template('error.html', error='Invalid request'), 400

	subdomain = session['csr-subdomain']

	try:
		csr = x509.load_pem_x509_csr(request.form['csr'].encode())
	except:
		return render_template('error.html', error='Invalid CSR!'), 400

	try:
		private_key = serialization.load_pem_private_key(request.form['priv'].encode(), password=None)
	except:
		return render_template('error.html', error='Invalid private key!'), 400

	if subdomain in manager.subdomains:
		return render_template('error.html', error='Subdomain already exists'), 400

	public_key = signer.generate(csr)

	manager.add(subdomain, public_key, private_key)

	session['subdomain'] = subdomain

	del session['csr-subdomain']

	return render_template('success.html', subdomain=subdomain)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	if 'subdomain' not in session:
		return render_template('error.html', error='Subdomain not found!'), 400

	if request.method == 'GET':
		subdomain = session['subdomain']
		with open(f'content/{subdomain}', 'rb') as f:
			content = f.read().decode(encoding='UTF-8')

		return render_template('edit.html', subdomain=subdomain, content=content)
	elif request.method == 'POST':
		if 'content' not in request.form:
			return render_template('error.html', error='No content')

		with open(f'content/{session["subdomain"]}', 'wb') as f:
			f.write(request.form['content'].encode())

		return render_template('updated.html')

@app.after_request
def security_headers(response):
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['Referrer-Policy'] = 'no-referrer'
	response.headers['Content-Security-Policy'] = f"default-src 'self' *.{config.DOMAIN}; script-src 'unsafe-inline' 'unsafe-eval'; style-src 'unsafe-inline'"
	return response
