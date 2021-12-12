#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
import uuid
import os

FLAG = os.environ.get('FLAG', 'X-MAS{test}')
ADMIN_COOKIE = os.environ.get('ADMIN_COOKIE')
SECRET_TOKEN = os.urandom(64).hex()

app = Flask (__name__)

quotes = [
    {'text': 'Man cannot live by bread alone; he must have <b>peanut butter</b>.', 'author': 'James A. Garfield'},
    {'text': 'He who can does - he who cannot, teaches.', 'author': 'George Bernard Shaw'},
    {'text': "I'd like to live like a poor man - only with lots of <i>money</i>.", 'author': 'Pablo Picasso'},
    {'text': 'So next I went to Russia three times, in late 2001 and 2002, to see if I could negotiate the purchase of two <strong>ICBMs</strong>', 'author': 'Elon Musk'}
]

pending_quotes = []

@app.route ('/', methods = ['GET'])
def index():
    return render_template ("index.html", quotes=quotes)


@app.route ('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template ("submit.html")

    quote = request.form.get('quote')
    author = request.form.get('author')
    if not isinstance(quote, str) or not isinstance(author, str) or len(quote) > 256 or len(quote) < 8 or len(author) > 32 or len(author) < 4:
        return 'NOPE'

    quote_obj = {
        'text': quote,
        'author': author
    }
    pending_quotes.append(quote_obj)
    return render_template ("submit.html", message=f"Quote submitted successfully.")


@app.route ('/quote/latest', methods = ['GET', 'POST'])
def quote():
    global pending_quotes
    if request.method == 'GET':
        if request.cookies.get('admin_cookie', False) != ADMIN_COOKIE or len(pending_quotes) == 0:
            return 'NOPE'
        q = pending_quotes[0]
        pending_quotes = pending_quotes[1:]
        print("Admin viewing quote: ", q)
        return render_template ("quote_review.html", quote=q, SECRET_TOKEN=SECRET_TOKEN)

    action = request.form.get('action')
    secret = request.form.get('secret')
    if not isinstance(action, str) or action not in ['APPROVE', 'REJECT'] or secret != SECRET_TOKEN:
        return 'NOPE'

    if action == "REJECT":
        return redirect("/list", code=302)

    return "You did it! Here's your reward: " + FLAG


if __name__ == '__main__':
    app.run (host = '127.0.0.1', port = 2000)
