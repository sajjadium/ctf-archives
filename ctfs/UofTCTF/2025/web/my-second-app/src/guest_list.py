from flask import Flask, request, render_template, render_template_string, flash, redirect, url_for
import hashlib
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
SECRET_KEY = os.urandom(random.randint(16, 64))
MALICIOUS_SUBSTRINGS = [
    '#','%', '!', '=', '+', '-', '/', '&', '^', '<', '>','and', 'or', 'not','\\', '[', ']', '.', "_",',',"0","1","2","3","4","5","6","7","8","9",'"', "'",'`','?',"attr","request","args","cookies","headers","files","form","json","flag",'lipsum','cycler','joiner','namespace','url_for','flash','config','session','dict','range','lower', 'upper', 'format', 'get', "item", 'key', 'pop', 'globals', 'class', 'builtins', 'mro',"True","False"
]

GUESTS = []

def good(name):
    if not all(ord(c) < 255 for c in name):
        return False
    for substring in MALICIOUS_SUBSTRINGS:
        if substring in name:
            return False
    return True

def load_guests():
    with open("./guests.txt", 'r') as f:
        for line in f:
            name = line.strip()
            if not name:
                continue
            assert good(name), f"Bad name: {name}"

            ticket = hashlib.sha256(SECRET_KEY + name.encode('latin-1')).hexdigest()

            GUESTS.append({
                "name": name,
                "ticket": ticket
            })

def verify_ticket(name, ticket):
    expected = hashlib.sha256(SECRET_KEY + name.encode('latin-1')).hexdigest()
    return expected == ticket

@app.route('/')
def index():
    return render_template('index.html', guests=GUESTS)

@app.route('/signin', methods=['POST'])
def signin():
    name = request.form.get('name')
    ticket = request.form.get('ticket')

    if not name or not ticket:
        flash("You must provide a name and ticket!", "warning")
        return redirect(url_for('index'))

    if verify_ticket(name, ticket):
        if not good(name):
            flash(f"The ticket for {name} has been revoked!", "danger")
            return redirect(url_for('index'))
        try:
            with open("./templates/welcome.html", 'r') as f:
                template_content = f.read()
            rendered_template = template_content % (name,)
            return render_template_string(rendered_template)
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('index'))
    else:
        flash(f"{name} is not invited!", "danger")
        return redirect(url_for('index'))
if __name__ == '__main__':
    load_guests()
    app.run(host='0.0.0.0', port=5000)