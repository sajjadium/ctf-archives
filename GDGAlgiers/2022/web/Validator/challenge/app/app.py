import os
from flask import Flask, request, redirect, render_template, session, send_from_directory
from dotenv import load_dotenv
from schema import Schema, And, SchemaError
import json

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("FLASK_ENV") == "development"

FLAG_DIRECTORY = "."
FLAG_FILENAME = "flag.txt"

# MyDict class

class MyDict(dict):
    def __getattr__(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    def __setattr__(self, *args, **kwargs):
        return self.__setitem__(*args, **kwargs)

# Utility functions

def wrap_error(e: Exception):
    return f"{e.__class__.__name__}: {e}"

# Routes

@app.route("/")
def index():
    session["isAdmin"] = False
    return render_template("index.html")

@app.route("/validate", methods=["POST", "GET"])
def validate():
    if request.method == "GET":
        return redirect("/")

    res = MyDict()

    json_body = request.json
    if type(json_body) != dict:
        res.message = "JSON body must be a dictionary"
        res.isError = True
        return res

    schema = json_body.get("schema")
    if type(schema) != dict:
        res.message = "Schema must be a dictionary"
        res.isError = True
        return res

    data = json_body.get("data")
    if type(data) != str:
        res.message = "Data must be a string"
        res.isError = True
        return res
    try:
        data = json.loads(data)
    except json.JSONDecodeError as e:
        res.message = wrap_error(e)
        res.isError = True
        return res

    valid_msg = json_body.get("validMsg", "Valid data")
    if type(valid_msg) != str:
        res.message = "Valid message must be a string"
        res.isError = True
        return res
    invalid_msg = json_body.get("invalidMsg", "Invalid data")
    if type(invalid_msg) != str:
        res.message = "Invalid message must be a string"
        res.isError = True
        return res

    types = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
    }
    if any(type(fname) != str for fname in schema):
        res.message = "Invalid field name"
        res.isError = True
        return res
    if any(ftype not in types for _, ftype in schema.items()):
        res.message = "Invalid field type"
        res.isError = True
        return res

    sdict = { fname: And(types[ftype]) for fname, ftype in schema.items() }
    s = Schema(sdict, error=invalid_msg)

    try:
        s.validate(MyDict(data))
        res.message = valid_msg
        res.isError = False
        return res
    except SchemaError as e:
        res.message = wrap_error(e)
        res.isError = True
        return res

@app.route("/flag")
def flag():
    if session.get("isAdmin", False):
        return send_from_directory(FLAG_DIRECTORY, FLAG_FILENAME)
    return redirect("/")

# Error handling

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
