import os
import sqlite3
import json

from flask import Flask, render_template, request, redirect, url_for, session
from bot import bot

SECRET_KEY = os.urandom(32).hex()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=('GET',))
def index():
    return redirect(url_for('form_builder'))

# Add 404 route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/form_builder', methods=('GET',))
def form_builder():
    session['csrf_token'] = os.urandom(32).hex()
    return render_template('form_builder.html')

@app.route('/form_builder', methods=('POST',))
def form_builder_post():
    if 'csrf_token' not in session or session['csrf_token'] != request.form['csrf_token']:
        return redirect(url_for('csrf_error.html'))
    formdata = request.form.to_dict()
    if 'csrf_token' in formdata:
        del formdata["csrf_token"]
    for key in formdata:
        session[key] = formdata[key]

    return redirect(url_for('view_form'))

@app.route('/view_data', methods=('GET',))
def view_form():
    formdata = {}
    for key in session:
        formdata[key] = session[key]
    del formdata["csrf_token"]
    return render_template('view_form.html', formdata=formdata)

@app.route('/bot', methods=('GET',))
def bot_route():
    return render_template('bot.html')

@app.route('/bot', methods=('POST',))
def bot_route_post():
    fields = request.form['fields']
    bot(fields)
    return redirect('/')

app.run(host='0.0.0.0', port=1337)