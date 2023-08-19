from flask import Flask, render_template, session, request, Response
from werkzeug.exceptions import HTTPException
import os
import json
import requests
from random import randint

def set_(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                set_(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            set_(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

class Board():
    def __init__(self): pass

    @property
    def pinned_content(self):
        return [{
            "title": "Our First Adventure!", 
            "text": "Today we went to the forest and you can't believe what we've got to! It's a house made out of gingerbread, cake and candy! How sweet it is!"
        }]
    
    current_content = []

    def save(self, data):
        data_ = json.loads(data)
        if "new_content" not in data_:
            raise Exception("There is nothing to save.")
        if not isinstance(data_["new_content"], list) and not len(data_["new_content"]) > 0 and not all([isinstance(x, dict) for x in data_["new_content"]]):
            raise Exception("\"new_content\" should be a non-empty list of JSON-like objects.")
        if not all(["title" in x and "text" in x for x in data_["new_content"]]):
            raise Exception("Please check your bulletin format")
        set_(data_, self)

    def load(self):
        res = self.pinned_content
        if isinstance(self.current_content, list) and len(self.current_content) > 0 and all(["title" in x and "text" in x for x in self.current_content]):
            res.extend(self.current_content)
        if hasattr(self, "new_content") and self.new_content is not None:
            new_content = getattr(self, "new_content")
            self.current_content.extend(new_content)
            res.extend(new_content)
            self.new_content = None
        return res[::-1]


app = Flask(__name__)
app.config["SECRET_KEY"] = str(os.urandom(32))
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.add_template_global(randint)

bulletin_board = Board()

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return str(e), 500

@app.after_request
def after_request_callback(response: Response):
    if response.status_code >= 500:
        updated = render_template("template.html", status=response.status_code, message=response.response[0].decode())
        response.set_data(updated)
    return response

@app.route("/<path:path>")
def render(path):
    if not os.path.exists(f"templates/{path}"):
        return render_template("template.html", status=404, message="not found")
    return render_template(f"{path}")

@app.route("/")
def index():
    session["user"] = "hansel & gretel"
    bulletins = requests.post("http://localhost:3000/load_bulletins").json()
    return render_template("index.html", bulletins=bulletins)

@app.route("/save_bulletins", methods=["POST"])
def save_bulletins():
    if not request.is_json:
        raise Exception("Only accept JSON.")
    bulletin_board.save(request.data)
    return {"message": "Bulletins saved."}, 200, {"Content-Type": "application/json"}

@app.route("/load_bulletins", methods=["POST"])
def load_bulletins():
    return bulletin_board.load(), 200, {"Content-Type": "application/json"}
        
@app.route("/flag")
def flag():
    if session.get("user") != "witch":
        return render_template("template.html", status=403, message="You are not the witch.")
    return render_template("template.html", status=200, message=os.environ["FLAG"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000")