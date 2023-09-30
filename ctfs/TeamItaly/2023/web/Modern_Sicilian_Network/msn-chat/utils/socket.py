import os
from time import sleep
from hashlib import sha256
from flask import session, request
from flask_socketio import (
    emit,
    send,
    rooms,
    SocketIO,
    join_room,
    ConnectionRefusedError
)
from .models import *
from .chatUtils import *

CHECKER_TOKEN = os.getenv("CHECKER_TOKEN")

socket = SocketIO()

@socket.on("connect")
def socket_connection():
    if not 'id' in session:
        raise ConnectionRefusedError("Unauthorized!")
    emit("connect_response", {"data": "Connected!"})


@socket.on("join")
def join_chat_room(receiver):
    if not isinstance(receiver, str):
        raise RuntimeError("Wrong type")
    sender = session["id"]
    room = ':'.join(sorted([sender, receiver]))
    join_room(room)
    sender = User.query.get(sender)
    receiver = User.query.get(receiver)
    messages_received = set(sender.messages).intersection(set(receiver.sent))
    messages_sent = set(sender.sent).intersection(set(receiver.messages))
    messages = list(messages_received.union(messages_sent))
    messages = sorted(messages, key=lambda d: d.timestamp)
    message_list = [{
        "id": message.id,
        "type": message.type,
        "sender": message.sender_id,
        "receiver": message.receiver_id,
        "content": message.content,
        "timestamp": message.timestamp.timestamp()
    } for message in messages]
    send({"messages": message_list}, to=room)
    emit_pow()


# type 0 = text
# type 1 = article
@socket.on("message")
def chat_message(msgType, content):
    if not isinstance(content, str) or not isinstance(msgType, int):
        raise RuntimeError("Wrong type")
    if len(content) > 512:
        return
    
    room = [r for r in rooms() if r != request.sid][0]
    if len(room.split(":")) != 2 or msgType not in [0, 1]:
        raise RuntimeError("Invalid parameters")
    
    receiver = User.query.get([x for x in room.split(":") if x != session["id"]][0])
    sender = User.query.get(session["id"])
    # nobody should be able to log in as them but i'll be careful anyway
    if sender.username in ["Loldemort", "Tofu"]:
        raise RuntimeError("Forbidden accounts")
    
    if msgType == 1:
        # articles sanity check
        if len(content) != 73 or content.count("/") != 1 or content.index("/") != 36 \
                or any([c not in "0123456789abcdef-/" for c in content]):
            return
    
    create_message(sender, receiver, msgType, content, room)


@socket.on("nudge")
def chat_nudge(powX):
    room = [r for r in rooms() if r != request.sid][0]
    sender = User.query.get(session["id"])
    # nobody should be able to log in as them but i'll be careful anyway
    if sender.username in ["Loldemort", "Tofu"]:
        raise RuntimeError("Forbidden accounts")
    emit("nudge", {"sender": sender.id}, to=room)

    # proof of work check
    complexity = 5
    target = sender.powTarget
    if powX != CHECKER_TOKEN and (not target or not sha256(f'{sender.powTarget}{powX}'.encode()).hexdigest()[:complexity] == '0' * complexity):
        return
    emit_pow()

    # let's bring the admin alive, after 3 seconds
    receiver = User.query.get([x for x in room.split(":") if x != session["id"]][0])
    if receiver == User.query.filter_by(username="Loldemort").first():
        sleep(3)
        admin_react_to_message(receiver, sender, room)


def emit_pow():
    user = User.query.get(session["id"])
    user.powTarget = sha256(os.urandom(24)).hexdigest()
    db.session.commit()
    emit("pow", {
        "target": user.powTarget,
        "complexity": 5
    })