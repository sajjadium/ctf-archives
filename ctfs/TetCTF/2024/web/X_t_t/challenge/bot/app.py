from flask import Flask, request, render_template
import os
import subprocess
from utils import *
import base64

app = Flask(__name__)
PORT = int(os.getenv('PORT', '5001'))
BIND_ADDR = os.getenv('BIND_ADDR', '0.0.0.0')
app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")


@app.route('/', methods=['POST'])
def add_task():
    id = request.form.get('id')
    title = request.form.get('title')
    content = request.form.get('content')
    msg = 'Error! Please notice admin'
    print(title,content)
    # Check valid id
    if is_valid_uuid(id):
        command = f"rm -rf /tmp/.X99-lock;export id='{base64.b64encode(id.encode('utf-8')).decode('utf-8')}'; export title='{base64.b64encode(title.encode('utf-8')).decode('utf-8')}' ;export content='{base64.b64encode(content.encode('utf-8')).decode('utf-8')}';/bin/sh /app/app/run.sh"
        print('[+] Executing: {}'.format(command))
        os.system(command)
        print('[+] Done: {}'.format(command))
    else:
        msg = 'Invalid Report Id'
    return msg


def main():
    app.run(host=BIND_ADDR, port=PORT)  # debug=True


if __name__ == '__main__':
    main()
