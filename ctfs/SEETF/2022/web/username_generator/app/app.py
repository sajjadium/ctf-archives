from flask import Flask, render_template, request
import socket
import os

app = Flask(__name__)
admin_ip = socket.gethostbyname("admin")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/flag')
def flag():
    if request.remote_addr == admin_ip:
        return os.environ["FLAG"]

    else:
        return "You are not admin!"


if __name__ == '__main__':
    app.run()
