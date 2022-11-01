from flask import Flask, request, jsonify
from tempfile import NamedTemporaryFile
import subprocess
import re

# Reference solution uses 140 lines of code, 250 should be well enough.
MAX_DECORATION = 250 

decorator_re = re.compile(r'^@[a-z._]+$', re.IGNORECASE)

app = Flask(__name__)

def checkCode(code):
    lines = code.strip().split("\n")
    if (len(lines) < 2):
        raise SyntaxError("The culinary class room need at least _some_ decoration.")
    if len(lines) > MAX_DECORATION:
        raise SyntaxError("This is too much, this culinary class room does not have THAT much space.")
    if (lines[-1] != "class room: ..."):
        raise SyntaxError("What are you trying to decorate?")
    for idx, line in enumerate(lines[:-1], start=1):
        if not line.strip():
          continue
        if not decorator_re.match(line):
            raise SyntaxError(f"You can't decorate with that! (line {idx})")


def runCode(code):
    with NamedTemporaryFile() as f:
        f.write(code.encode('utf-8'))
        f.flush()
        return subprocess.check_output(['python3', f.name], timeout=.1).decode()


@app.route('/api/submit', methods=['POST'])
def submit():
    code = request.get_json().get('code', '')
    try:
        checkCode(code)
        output = runCode(code)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'output': f"ERROR: {e}"})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

