from flask import Flask, request, render_template, redirect, session, send_from_directory
from functools import wraps
import redis
from werkzeug.utils import secure_filename
import requests
import urllib.parse

from configuration import *

app = Flask(__name__, static_folder='static/', static_url_path='/')
app.secret_key = os.urandom(128)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True, # default flask behavior just does this
    SESSION_COOKIE_SAMESITE='None',
)

## redis is used for rate-limiting on the bot. Not intended part of solution, you can ignore.
r = redis.Redis(host='redis')

# Authentication decorator
def vie_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not session.get('auth', False): 
            return render_template("error.html", error="Sorry, you need to be logged in to access this.")
        return f(*args, **kwargs)
    return decorator

@app.route("/")
def base():
    if session.get('auth'):
        return render_template("admin.html")
    return render_template("index.html")

@app.route("/visit", methods=["GET", "POST"])
def visit_handler():
    if request.method == "GET":
        return render_template("visit.html")
    elif request.method == "POST":
        url = request.form.get('url')
        if url == '':
            return render_template("error.html", error="The URL cannot be blank!")
        elif url.startswith(('http://', 'https://')):
            r.rpush('submissions', url)
            return "Submitted"
        else: 
            return render_template("error.html", error="The URL can only be HTTP(S)!")
                            

@app.route("/login", methods=["GET", "POST"])
def login_handler():
    if request.method == "GET":
        if session.get('auth'):
            return redirect('/')
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if username == ADMIN_NAME and password == ADMIN_PASSWORD:
            session['auth'] = True
            return redirect("/")
        else: 
            return render_template("error.html", error="You're not Vie.")
        

@app.route("/characters")
@vie_auth
def character_handler():
    r = requests.get(GRAPHQL_ENDPOINT + "?query={query}".format(query=urllib.parse.quote(QUERY)))
    # TODO: PARSE better
    return r.json()['data']['getCharacters']['edges']
    
@app.route("/view/<string:img>")
@vie_auth
def img_handler(img):
    return send_from_directory('uploads', img)
    
@app.route("/newchar", methods=["GET", "POST"])
@vie_auth
def upload_handler():
    if request.method == "GET":
        return render_template("newchar.html")
    elif request.method == "POST":
        name = request.form.get('name')
        occupation = request.form.get('occupation')
        cursed_technique = request.form.get('cursed_technique')
        notes = request.form.get('notes')
        upload = request.files.get('file')

        if upload is None:
            return render_template("error.html", error="You can't upload an empty file!")

        ext = upload.filename.split(".")[-1]
        
        if ext != "png":
            return render_template("error.html", error="I see what you're trying to do.")

        filename = secure_filename(os.urandom(42).hex())

        mutation = MUTATION.format(name=name, occupation=occupation, cursed_technique=cursed_technique, notes=notes, ct=cursed_technique)

        r = requests.post(GRAPHQL_ENDPOINT, json={"query": mutation, "variables": None})

        if (r.json()["data"]["addNewCharacter"]['status'] == True):
            upload.save(f"uploads/{filename}.{ext}")
            return redirect(f"/view/{filename}.{ext}")
        else:
            return render_template("error.html", error="Something went wrong when trying to upload through graphql!")

def main():
    app.run(port=PORT, debug=False, host='0.0.0.0')


if __name__ == "__main__":
    main()
