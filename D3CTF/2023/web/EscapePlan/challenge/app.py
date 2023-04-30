import base64

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def challenge_3():
    cmd = request.form.get("cmd", "")
    if not cmd:
        return """<pre>
import requests, base64
exp = ''
requests.post("", data={"cmd": base64.b64encode(exp.encode())}).text
</pre>
"""

    try:
        cmd = base64.b64decode(cmd).decode()
    except Exception:
        return "bad base64"

    black_char = [
        "'", '"', '.', ',', ' ', '+',
        '__', 'exec', 'eval', 'str', 'import',
        'except', 'if', 'for', 'while', 'pass',
        'with', 'assert', 'break', 'class', 'raise',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ]
    for char in black_char:
        if char in cmd:
            return f'failed: `{char}`'

    msg = "success"
    try:
        eval(cmd)
    except Exception:
        msg = "error"

    return msg
