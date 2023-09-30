import os
import uuid
import random
import requests
from datetime import datetime
from flask_socketio import send
from .db import *
from .models import *

def create_message(sender, receiver, msgType, content, room):
    message = Message(
        str(uuid.uuid4()),
        msgType,
        content,
        datetime.utcnow(),
        receiver,
        sender
    )
    db.session.add(message)
    db.session.commit()
    send({"messages": [{
        "id": message.id,
        "type": message.type,
        "sender": message.sender_id,
        "receiver": message.receiver_id,
        "content": message.content,
        "timestamp": message.timestamp.timestamp()
    }]}, to=room)



### ADMIN BOT LOGIC - don't waste your time here
DOMAIN = os.getenv("DOMAIN")
HEADLESS_HOST = os.getenv("HEADLESS_HOST")
HEADLESS_PORT = os.getenv("HEADLESS_PORT")
HEADLESS_AUTH = os.getenv("HEADLESS_AUTH")
CHAT_PORT = os.getenv("CHAT_PORT")
SPACES_PORT = os.getenv("SPACES_PORT")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

AUTOMATED_REPLIES = {
    "nothing": [
        "what's up?",
        "yeah?",
        "tell me"
    ],
    "text": [
        "sorry can't answer now, tofu ate my homework",
        "don't you think Tofu is a beautiful cat?",
        "i love Tofu!! he tries to lick my hair sometimes but he's the cutest",
        "have you tried rebooting your computer??",
        "eating an arancina would solve your problems, or maybe most of them",
        "i ain't reading all that, happy for you tho, or sorry that happened"
    ],
    "article": [
        "i love reading blogs! i'll read that soon",
        "seems interesting! gonna read it asap",
        "oh my, is it a new Team Italy CTF writeup?! i'm opening that link rn!!!"
    ]
}

def admin_react_to_message(admin, user, room):
    messages = sorted(list(set(user.sent).intersection(set(admin.messages))), key=lambda d: d.timestamp)

    if len(messages) == 0:
        create_message(admin, user, 0, random.choice(AUTOMATED_REPLIES["nothing"]), room)
        return

    last_user_message = messages[-1]
    if last_user_message.type != 1: # text
        create_message(admin, user, 0, random.choice(AUTOMATED_REPLIES["text"]), room)
    else: # article
        CHAT_PORT_SUFFIX = "" if int(CHAT_PORT) == 80 else f":{CHAT_PORT}"
        SPACES_PORT_SUFFIX = "" if int(SPACES_PORT) == 80 else f":{SPACES_PORT}"
        requests.post(
            f"http://{HEADLESS_HOST}:{HEADLESS_PORT}",
            json = {
                "actions": [
                    {
                        "type": "request",
                        "method": "POST",
                        "url": f"http://chat.{DOMAIN}{CHAT_PORT_SUFFIX}/api/v1/session",
                        "data": '{"username":"Loldemort","password":"%s"}' % ADMIN_PASSWORD,
                        "headers": { "Content-Type": "application/json" },
                        "timeout": 5
                    },
                    {
                        "type": "request",
                        "method": "GET",
                        "url": f"http://spaces.{DOMAIN}{SPACES_PORT_SUFFIX}/articles/{last_user_message.content}",
                        "timeout": 15
                    }
                ]
            },
            headers = {
                "X-Auth": HEADLESS_AUTH
            },
            timeout = 5
        )
        create_message(admin, user, 0, random.choice(AUTOMATED_REPLIES["article"]), room)