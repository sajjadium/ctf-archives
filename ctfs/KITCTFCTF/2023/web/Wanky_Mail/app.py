from flask import Flask, render_template_string, request, redirect, abort
from aiosmtpd.controller import Controller
from datetime import datetime
from base58 import b58decode, b58encode
import random 
import string
import os
from datetime import datetime
import queue

mails = {}
active_addr = queue.Queue(1000)

def format_email(sender, rcpt, body, timestamp, subject):
    return {"sender": sender, "rcpt": rcpt, 'body': body, 'subject': subject, "timestamp": timestamp}

def render_emails(address):
    id = 0
    render = """
    <table>
        <tr>
            <th id="th-left">From</th>
            <th>Subject</th>
            <th id="th-right">Date</th>
        </tr>
    """
    overlays = ""
    m = mails[address].copy()
    for email in m:

        render += f"""
        <tr id="{id}">
            <td>{email['sender']}</td>
            <td>{email['subject']}</td>
            <td>{email['timestamp']}</td>
        </tr>
        """
        overlays += f"""
        <div id="overlay-{id}" class="overlay">
            <div class="email-details">
                <h1>{email['subject']} - from: {email['sender']} to {email['rcpt']}</h1>
                <p>{email['body']}</p>
            </div>
        </div>
        """
        id +=1
    render += "</table>"
    render += overlays
    return render


def get_emails(id):
    with open('templates/index.html') as f:
        page = f.read()
        return page.replace('{{$}}', render_emails(id))

def log_email(session, envelope):
    print(f'{session.peer[0]} - - {repr(envelope.mail_from)}:{repr(envelope.rcpt_tos)}:{repr(envelope.content)}', flush=True)

def esc(s: str):
    return "{% raw %}" + s + "{% endraw %}"

class Handler:
     async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith(os.environ.get('HOSTNAME')):
             return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        print(address, flush=True)
        return '250 OK'

     async def handle_DATA(self, server, session, envelope):
        m = format_email(esc(envelope.mail_from), envelope.rcpt_tos[0], esc(envelope.content.decode()), datetime.now().strftime("%d-%m-%Y, %H:%M:%S"), "PLACEHOLDER")
        log_email(session, envelope)
        r = envelope.rcpt_tos[0]
        if not mails.get(r):
            if active_addr.full():
                mails.pop(active_addr.get())
            mails[r] = []
            active_addr.put(r)
        if len(mails[r]) > 10:
            mails[r].pop(0)
        mails[r].append(m)
        return '250 OK'

c = Controller(Handler(), "0.0.0.0")
c.start()


app = Flask(__name__)
@app.route('/')
def index():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
    address = f"{username}@{os.environ.get('HOSTNAME', 'example.com')}"
    if not address in mails.keys():
        if active_addr.full():
            del mails[active_addr.get()]
        mails[address] = []
        active_addr.put(address)
    id = b58encode(address).decode()
    return redirect("/" + id)

@app.route('/<id>')
def mailbox(id):
    address = b58decode(id).decode()
    if not address in mails.keys():
        abort(404)    
    return render_template_string(get_emails(address), address=address)

if __name__ == '__main__':
    app.run()
