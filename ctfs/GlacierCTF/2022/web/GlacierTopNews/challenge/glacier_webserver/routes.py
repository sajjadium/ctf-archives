import os

import flask
from flask.templating import TemplateNotFound
from config import app
from flask import render_template
from flask import send_from_directory
from glacier_webserver.utils import render_template_with_wrapper
from glacier_webserver.utils import require_jwt


@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
def render_error(error):
    return render_template('error/404.html'), 404


@app.route('/session/logout')
def sessionLogout():
    return flask.redirect('/', code=302)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def render_index(path):
    page = path
    if page == '':
        page = '/index'
    return render_template_with_wrapper('page', page)


@app.route('/admin', defaults={'path': ''})
@app.route('/<path:path>')
@require_jwt
def render_admin(path):
    page = path
    if page == '':
        page = '/index'
    return render_template_with_wrapper('admin', page)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(
            app.root_path,
            'static'
        ),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )
