from flask import Flask, render_template, request, redirect, url_for, make_response
import jwt
import datetime
from utils import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '**REDACTED**'


flags = {1:
         {
            "name": "dummy flag",
            "description": "you don't really need this flag",
            "content": "**REDACTED**",
            "price": 3.99,
    },
    2:  {
            "name": "Okay Flag",
            "description": "at least it's leet",
            "content":"**REDACTED**",
            "price": 9.99,
        },
    3: {
            "name": "The real flag",
            "description": "I'm telling you neeed this",
            "content":"**REDACTED**",
            "price": 40.99,
        }
    }


@app.route('/')
def home():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))

    try:
        token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = token["username"]
        return render_template('home.html', flags=flags, balance=getBalance(username))
    except Exception as e:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    token = request.cookies.get('token')
    if token:
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            return redirect(url_for('home'))
        except:
            pass

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if checkUser(username, password):
            token = jwt.encode({
                'username': username,
                'ticket_regex': generateTicket(username),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            response = make_response(redirect(url_for('home')))
            response.set_cookie('token', token)
            return response
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not addUser(username, password):
            return render_template('register.html', error='Username already taken')

        token = jwt.encode({
            'username': username,
            'ticket_regex': generateTicket(username),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        response = make_response(redirect(url_for('home')))
        response.set_cookie('token', token)
        return response

    return render_template('register.html')

@app.route('/buy-flag/<int:flag_id>')
def buy_flag(flag_id):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    try:
        token_content = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = token_content["username"]
        ticket_regex = token_content["ticket_regex"]
    except Exception as e:
        return redirect(url_for('login'))
    
    if flag_id not in flags or not checkBalance(username, flags[flag_id]["price"]) :
        return redirect(url_for('home'))
    
    updateBalance(username, flags[flag_id]["price"])
    return render_template("home.html",flags=flags, message=flags[flag_id]["content"], balance=getBalance(username))


@app.route('/redeem', methods=['POST'])
def redeem():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    
    try:
        ticket = request.form["ticket"]
        token_content = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username, regex = token_content["username"], token_content["ticket_regex"]
        if checkRedeem(username) and checkTicket(regex, ticket):
            userRedeem(username)
            return render_template("home.html", flags=flags, message="Ticket redeemed", balance=getBalance(username))
        else:
            return render_template("home.html", flags=flags, message="Can't redeem ticket", balance=getBalance(username))

    
    except Exception as e:
        return redirect(url_for('login'))
