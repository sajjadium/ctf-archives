from flask import Flask, request, render_template, redirect
from ast import parse
import re
import subprocess
import uuid

app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload')
def upload():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'file' not in request.files:
        return redirect('/')
    f = request.files['file']
    fname = f"uploads/{uuid.uuid4()}.py"
    f.save(fname)
    code_to_test = re.sub(r'\\\s*\n\s*', '', open(fname).read().strip())
    if not code_to_test:
        return redirect('/')
    tested = test_code(code_to_test)
    if tested[0]:
        res = ''
        try:
            ps = subprocess.run(['python', fname], timeout=5, capture_output=True, text=True)
            res = ps.stdout
        except:
            res = 'code timout'
        return render_template('submit.html', code=code_to_test.split('\n'), text=res.strip().split('\n'))
    else:
        return render_template('submit.html', code=code_to_test.split('\n'), text=[tested[1]])

@app.route('/static/<path:path>')
def static_file(filename):
    return app.send_static_file(filename)

def test_for_non_ascii(code):
    return any(not (0 < ord(c) < 127) for c in code)

def test_for_imports(code):
    cleaned = clean_comments_and_strings(code)
    return 'import ' in cleaned

def test_for_invalid(code):
    if len(code) > 1000:
        return True
    try:
        parse(code)
    except:
        return True
    return False

blocked = ["__import__", "globals", "locals", "__builtins__", "dir", "eval", "exec",
        "breakpoint", "callable", "classmethod", "compile", "staticmethod", "sys",
        "__importlib__", "delattr", "getattr", "setattr", "hasattr", "sys", "open"]

blocked_regex = re.compile(fr'({"|".join(blocked)})(?![a-zA-Z0-9_])')

def test_for_disallowed(code):
    code = clean_comments_and_strings(code)
    return blocked_regex.search(code) is not None

def test_code(code):
    if test_for_non_ascii(code):
        return (False, 'found a non-ascii character')
    elif test_for_invalid(code):
        return (False, 'code too long or not parseable')
    elif test_for_imports(code):
        return (False, 'found an import')
    elif test_for_disallowed(code):
        return (False, 'found an invalid keyword')
    return (True, '')

def clean_comments_and_strings(code):
    code = re.sub(r'[rfb]*("""|\'\'\').*?\1', '', code,
                  flags=re.S)
    lines, res = code.split('\n'), ''
    for line in lines:
        line = re.sub(r'[rfb]*("|\')(.*?(?!\\).)?\1',
                      '', line)
        if '#' in line:
            line = line.split('#')[0]
        if not re.fullmatch(r'\s*', line):
          res += line + '\n'
    return res.strip()

if __name__ == '__main__':
    app.run(debug=True)
