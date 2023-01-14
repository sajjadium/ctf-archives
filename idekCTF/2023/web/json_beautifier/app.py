from flask import Flask, send_file

app = Flask(__name__)

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "script-src 'unsafe-eval' 'self'; object-src 'none';"
    return response


@app.route('/')
def index():
    return send_file('index.html')

app.run('0.0.0.0', 1337)
