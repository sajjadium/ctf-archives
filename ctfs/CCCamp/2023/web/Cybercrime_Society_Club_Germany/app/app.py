from flask import Flask, request, make_response, render_template, redirect, url_for
import json
from uuid import uuid4 as uuid
import random
import string
import hashlib
import time
from Userdb import UserDB
import subprocess

# Look Ma, I wrote my own web app!

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',)

userdb = UserDB("userdb.json")
userdb.add_user("admin@cscg.de", 9_001_0001, str(uuid())) 
# print(userdb.get_db())

## Helper Functions 

def check_activation_code(activation_code):
    # no bruteforce
    time.sleep(20)
    if "{:0>4}".format(random.randint(0, 10000)) in activation_code:
        return True
    else:
        return False


def delete_accs(emails):
    for email in emails:
        userdb.delete_user(email)
    return True


def error_msg(msg):
    resp = {
        "return": "Error",
        "message": msg
    }
    return json.dumps(resp)


def success_msg(msg):
    resp = {
        "return": "Success",
        "message": msg
    }
    return json.dumps(resp)
    

def get_user(request):
    auth = request.cookies.get("auth")
    if auth is not None:
        return userdb.authenticate_user(auth)
    return None


def validate_command(string):
    return len(string) == 4 and string.index("date") == 0


## API Functions

def api_create_account(data, user):
    dt = data["data"]
    email = dt["email"]
    password = dt["password"]
    groupid = dt["groupid"]
    userid=dt["userid"]
    activation = dt["activation"]

    if email == "admin@cscg.de":
        return error_msg("cant create admin")

    assert(len(groupid) == 3)
    assert(len(userid) == 4)

    userid = json.loads("1" + groupid + userid)
    # print(dt)
    # print(userid)

    if not check_activation_code(activation):
        return error_msg("Activation Code Wrong")
    # print("activation passed")


    if userdb.add_user(email, userid, password):
        # print("user created")
        return success_msg("User Created")
    else:
        return error_msg("User creation failed")


def api_delete_account(data, user):
    if user is None:
        return error_msg("not logged in")

    if data["data"]["email"] != user["email"]:
        return error_msg("Hey thats not your email!")

    # print(list(data["data"].values()))
    if delete_accs(data["data"].values()):
        return success_msg("deleted account")


def api_edit_account(data, user):
    if user is None:
        return error_msg("not logged in")
    
    new = data["data"]["email"]

    if userdb.change_user_mail(user["email"], new):
        return success_msg("Success")
    else:
        return error_msg("Fail")


def api_login(data, user):
    if user is not None:
        return error_msg("already logged in")

    c = userdb.login_user(data["data"]["email"], data["data"]["password"])
    if c is None:
        return error_msg("Wrong User or Password")
    resp = make_response(success_msg("logged in"))
    resp.set_cookie("auth", c)
    return resp


def api_logout(data, user):
    if user is None:
        return error_msg("Already Logged Out")

    userdb[user["email"]]["cookie"] = ""
    userdb.save_db()

    return True
    return render_template('logout.html', title="Logout", user=user)

def api_error(data, user):
    return error_msg("General Error")

def api_admin(data, user):
    if user is None:
        return error_msg("Not logged in")
    is_admin = userdb.is_admin(user["email"])
    if not is_admin:
        return error_msg("User is not Admin")

    cmd = data["data"]["cmd"]
    # currently only "date" is supported
    if validate_command(cmd):
        out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return success_msg(out.stdout.decode())


    return error_msg("invalid command")


actions = {
    "delete_account": api_delete_account,
    "create_account": api_create_account,
    "edit_account": api_edit_account,
    "login": api_login,
    "logout": api_logout,
    "error": api_error,
    "admin": api_admin,
}

## Routes

@app.route("/json_api", methods=["GET", "POST"])
def json_api():
    user = get_user(request)
    if request.method == "POST":
        data = json.loads(request.get_data().decode())
        # print(data)
        action = data.get("action")
        if action is None:
            return "missing action"

        return actions.get(action, api_error)(data, user)

    else:
        return json.dumps(user)

@app.route("/")
def home():
    user = get_user(request)
    if user is not None:
        return redirect(url_for("user"))
    return render_template('home.html', title="Home", user=None)

@app.route("/login")
def login():
    user = get_user(request)
    if user is not None:
        return redirect(url_for("user"))
    return render_template('login.html', title="Login", user=None)

@app.route("/signup")
def signup():
    user = get_user(request)
    if user is not None:
        return redirect(url_for("user"))
    return render_template('signup.html', title="Signup", user=None)

@app.route("/admin")
def admin():
    user = get_user(request)
    if user is None:
        return redirect(url_for("login"))
    # print(user)
    is_admin = userdb.is_admin(user["email"])
    if not is_admin:
        return redirect(url_for("user"))
    return render_template('admin.html', title="Admin", user=user)

@app.route("/user")
def user():
    user = get_user(request)
    if user is None:
        return redirect(url_for("login"))
    # print(user)
    is_admin = userdb.is_admin(user["email"])
    return render_template('user.html', title="User Page", user=user, is_admin=is_admin)

@app.route("/usersettings")
def settings():
    user = get_user(request)
    if user is None:
        return redirect(url_for("login"))
    return render_template('usersettings.html', title="User Settings", user=user)


app.run(host='0.0.0.0', port=1024, debug=False)

