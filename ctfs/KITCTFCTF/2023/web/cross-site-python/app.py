from flask import Flask, redirect, make_response, render_template, request, abort, Response
from base64 import b64decode as decode
from base64 import b64encode as encode
from queue import Queue
import random
import string

app = Flask(__name__)
projects  = {}
project_queue = Queue(1000)

def generate_id():
    return ''.join(random.choice(string.digits) for i in range(15))

@app.after_request
def add_csp(res):
    res.headers['Content-Security-Policy'] = "script-src 'self' 'wasm-unsafe-eval'; object-src 'none'; base-uri 'none';"
    return res

@app.route('/')
def index():
    return redirect("/new")

@app.route("/new")
def new():
    if project_queue.full():
        projects.pop(project_queue.get())
    new_id = generate_id()
    while new_id in projects.keys():
        new_id = generate_id()
    projects[new_id] = 'print("Hello World!")'
    project_queue.put(new_id)
    return redirect(f"/{new_id}/edit")

@app.route("/<code_id>/edit")
def edit_page(code_id):
    if code_id not in projects.keys():
        abort(404)
    
    code = projects.get(code_id)
    return render_template("edit.html", code=code)

@app.route('/<code_id>/save', methods=["POST"])
def save_code(code_id):
    code = request.json["code"]
    projects[code_id] = code
    return {"status": "success"}

@app.route('/<code_id>/exec')
def code_page(code_id):
    if code_id not in projects.keys():
        abort(404)

    code = projects.get(code_id)

    # Genius filter to prevent xss
    blacklist = ["script", "img", "onerror", "alert"]
    for word in blacklist:
        if word in code:
            # XSS attempt detected!
            abort(403)

    res = make_response(render_template("code.html", code=code))
    return res


if __name__ == '__main__':
    app.run()
