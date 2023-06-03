import os
import ssl
from smtplib import SMTP
from flask import Flask, request
import traceback

ctx = ssl.create_default_context(cafile='cert.pem')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    addr = request.form.get('addr', '')
    if request.method == 'POST':
        s = SMTP()
        try:
            s._host = 'localhost'
            s.connect(addr)
            s.starttls(context=ctx)
            s.sendmail('innocent-sender@nosuchdomain.example', ['innocent-recipient@nosuchdomain.example'],
f'''\
From: some-sender@nosuchdomain.example
To: some-recipient@nosuchdomain.example
Subject: [CONFIDENTIAL] Secret unlock code

Hi Recipient!
Sorry for the delay.  The code you asked for: {os.environ['FLAG']}

Stay safe,
Sender
''')
        except Exception:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return 'ok'
    return f'<form method=POST><input name=addr placeholder=address value={addr}><input type=submit>'
