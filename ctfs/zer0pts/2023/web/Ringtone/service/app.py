import flask
import os
import re
import ipaddress

FLAG= os.environ["FLAG"]
app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
RANDOM=os.environ["RANDOM"]
@app.route("/", methods=['GET'])
def index():
    resp = flask.make_response(flask.render_template("index.html"))
    resp.headers['Content-Security-Policy'] = \
        "script-src 'self' https://cdn.jsdelivr.net;" \
        "object-src 'none';" \
        "base-uri 'none';" 
    return resp
@app.route("/"+RANDOM, methods=['GET'])
def flag():
    if ipaddress.ip_address(flask.request.remote_addr) in ipaddress.ip_network('10.103.0.0/16'):
        resp = flask.make_response(FLAG)
        return resp
    else:
        resp = flask.make_response("You are not supposed to be here")
        return resp

if __name__ == '__main__':
    app.run(debug=False)
