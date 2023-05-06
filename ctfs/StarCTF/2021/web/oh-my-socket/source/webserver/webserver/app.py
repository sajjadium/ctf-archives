from flask import Flask, render_template, request
from subprocess import STDOUT, check_output
import os

app = Flask(__name__)


@app.route('/')
def index():
    return open(__file__).read()


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(f.filename))

        try:
            output = check_output(['python3', f.filename], stderr=STDOUT, timeout=80)
            content = output.decode()

        except Exception as e:
            content = e.__str__()

        os.system(' '.join(['rm', f.filename]))
        return content


if __name__ == '__main__':
   app.run(port=5000, host='0.0.0.0')