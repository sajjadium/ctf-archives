from flask import Flask, request, redirect
from bs4 import BeautifulSoup
import secrets
import base64

app = Flask(__name__)
SAFE_TAGS = ['i', 'b', 'p', 'br']

with open("home.html") as home:
    HOME_PAGE = home.read()

@app.route("/")
def home():
    return HOME_PAGE

@app.route("/add", methods=['POST'])
def add():
    contents = request.form.get('contents', "").encode()
    
    return redirect("/page?contents=" + base64.urlsafe_b64encode(contents).decode())

@app.route("/page")
def page():
    contents = base64.urlsafe_b64decode(request.args.get('contents', '')).decode()
    
    tree = BeautifulSoup(contents)
    for element in tree.find_all():
        if element.name not in SAFE_TAGS or len(element.attrs) > 0:
            return "This HTML looks sus."

    return f"<!DOCTYPE html><html><body>{str(tree)}</body></html>"

