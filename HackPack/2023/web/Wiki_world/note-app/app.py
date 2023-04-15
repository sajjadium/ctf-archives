from flask import *

app = Flask(__name__)

@app.route('/')
def default():
    return send_file('index.html')

@app.route('/<path:path>')
def send_artifacts(path):
    return send_from_directory('', path)
if __name__ == '__main__':
    app.run(host='0.0.0.0')