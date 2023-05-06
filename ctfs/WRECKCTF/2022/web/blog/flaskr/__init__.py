import os

from flask import Flask, abort

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=open("flaskr/protected/burdellsecrets.txt").read(),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db
db.init_db()

@app.route('/flaskr/protected/<path:filename>')
def protected(filename):
    if os.path.exists(os.path.join(app.root_path, 'protected', filename)):
        abort(403)
    else:
        abort(404)

from . import auth
app.register_blueprint(auth.bp)

from . import blog
app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')
