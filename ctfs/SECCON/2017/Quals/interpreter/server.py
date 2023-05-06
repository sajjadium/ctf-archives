import os
import random
import tempfile
import re
from uuid import uuid4

from flask import Flask, abort, render_template, request

app = Flask(__name__)
root = os.path.dirname(os.path.abspath(__file__))
upload_dir = os.path.join(root, 'upload')
interpreter = os.path.join(root, 'interpreter.py')
temp_dir = '/tmp/relativity'
FLAG = 'SECCON{??????????????????????}'

if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)


def parse_time(output):
    for line in output.split('\n'):
        match = re.match('^user\t([0-9]+m)?([0-9]+\.[0-9]{3}s)$', line)
        if match:
            m = match.group(1)
            if m[-1] == 's':
                r = float(m[:-1])
            elif m[-1] == 'm':
                r = float(m[:-1]) * 60
                r += float(match.group(2)[:-1])
            return r
    return 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_script():
    script = request.files.get('script')
    if script is None:
        return abort(400)

    filename = str(uuid4())

    script_path = os.path.join(upload_dir, filename)
    script.save(script_path)

    make_temp = lambda: tempfile.mktemp(prefix='%s_' % filename, dir=temp_dir)
    tmp = make_temp()
    tmp2 = make_temp()
    cmd = 'bash -c "time timeout 20 python %s %s" 1>%s 2>%s' % (interpreter, script_path, tmp, tmp2)
    os.system(cmd)

    with open(tmp, 'r') as f:
        output = f.read()

    with open(tmp2, 'r') as f:
        times = f.read()

    os.system('rm -f %s %s %s' % (tmp, tmp2, script_path))

    t = parse_time(times)
    output += '\n==STDERR==\n' + times + '\nTime: ' + str(t)
    if t >= 100:
        return output + '\nCongratulations! Here is your flag: ' + FLAG

    return output


if __name__ == '__main__':
    app.run(
        debug=True,
        use_reloader=True,
        host='0.0.0.0',
        port=5000,
    )
