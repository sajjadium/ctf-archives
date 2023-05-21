from flask import Flask, request, render_template, redirect, flash
from adminbot import visit
from urllib.parse import quote

app = Flask(__name__)

BASE_URL = "http://localhost:5000/"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    
    message = request.form.get('message')
    if len(message) == 0:
        flash("Please enter a message")
        return render_template('index.html')

    link = f"/ticket?message={quote(message)}"

    # Admin vists the link here
    visit(BASE_URL, f"{BASE_URL}{link}")

    return redirect(link)


@app.route('/ticket', methods=['GET'])
def ticket_display():
    message = request.args.get('message')
    return render_template('ticket.html', message=message)
