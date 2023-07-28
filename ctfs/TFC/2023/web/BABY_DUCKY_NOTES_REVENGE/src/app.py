from flask import Flask, jsonify
from routes import web, api
import database.database as db
import os, datetime


app = Flask(__name__)
app.secret_key = os.urandom(30).hex()
app.config['LOG_DIR'] = './static/logs/'

db.db_init()

app.register_blueprint(web, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')


@app.errorhandler(404)
def not_found(e):
    return e, 404

@app.errorhandler(403)
def forbidden(e):
    return e, 403

@app.errorhandler(400)
def bad_request(e):
    return e, 400

@app.errorhandler(401)
def bad_request(e):
    return e, 401

@app.errorhandler(Exception)
def handle_error(e):
    if not e.args or "username" not in e.args[0].keys():
        return e, 500
    
    error_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post = e.args[0]
    log_message = f'"{error_date}" {post["username"]} {post["content"]}'

    with open(f"{app.config['LOG_DIR']}{error_date}.txt", 'w') as f:
        f.write(log_message)

    return log_message, 500

app.run(host='0.0.0.0', port=1337, debug=False)
