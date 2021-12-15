from flask import Flask, render_template, render_template_string, request
import os
import utils


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CTFUA{REDACTED}'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return 'Under Construction...'


@app.route('/users')
def users():
    username = request.args.get('user', '<User>')
    if utils.filter(username):
        return render_template_string('Hello ' + username + '!')
    else:
        return 'Hello ' + username  + '!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

