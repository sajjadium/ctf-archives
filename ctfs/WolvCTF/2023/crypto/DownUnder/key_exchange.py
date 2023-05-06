from flask import Flask, request, jsonify
from json import loads
from Crypto.Util.number import long_to_bytes, bytes_to_long
from hashlib import sha256
from hmac import new
from uuid import uuid4
from generate import generate

app = Flask(__name__)

key = {
    '0' : 0 , '1' : 1 , '2' : 2 , '3' : 3 , '4' : 4 , '5' : 5 , '6' : 6 ,
    'a' : 70, 'b' : 71, 'c' : 72, 'd' : 73, 'e' : 74, 'f' : 75, 'g' : 76, 'h' : 77, 'i' : 78, 'j' : 79, 
    'k' : 80, 'l' : 81, 'm' : 82, 'n' : 83, 'o' : 84, 'p' : 85, 'q' : 86, 'r' : 87, 's' : 88, 't' : 89, 
    'u' : 90, 'v' : 91, 'w' : 92, 'x' : 93, 'y' : 94, 'z' : 95, '_' : 96, '{' : 97, '}' : 98, '!' : 99, 
}

sessions = {}

def bytes_to_long_flag(bytes_in):
    long_out = ''
    for b in bytes_in:
        long_out += str(key[chr(b)])
    return int(long_out)

def long_to_bytes_flag(long_in):
    new_map = {v: k for k, v in key.items()}
    list_long_in = [int(x) for x in str(long_in)]
    str_out = ''
    i = 0
    while i < len(list_long_in):
        if list_long_in[i] < 7:
            str_out += new_map[list_long_in[i]]
        else:
            str_out += new_map[int(str(list_long_in[i]) + str(list_long_in[i + 1]))]
            i += 1
        i += 1
    return str_out.encode("utf_8")

def diffie_hellman(A, g, b, p):
    B = pow(g,b,p)
    s = pow(A,b,p)
    message = b'My totally secure message to Alice'
    password = long_to_bytes(s)
    my_hmac = new(key=password, msg = message, digestmod=sha256)
    return str(bytes_to_long(my_hmac.digest())), B

@app.route("/")
def home():
    old_session = request.cookies.get('session')
    A = request.args.get('A', type = int)
    if not isinstance(A, int):
        return "Missing required query string parameter: A"
    if not old_session:
        p, q, g = generate()
        session = {"id": uuid4().hex, 'p': p, 'q': q, 'g': g, "attempts": 0}
        sessions[session['id']] = session
    else:
        if old_session not in sessions.keys():
            return "Invalid session"
        if not sessions[old_session]['attempts'] < 7:
            sessions.pop(old_session)
            return "Too many attempts"
        p, q, g, attempts = sessions[old_session]['p'], sessions[old_session]['q'], sessions[old_session]['g'], sessions[old_session]['attempts']
        session = {"id": old_session, 'p': p, 'q': q, 'g': g, "attempts": attempts + 1}
        sessions[old_session] = session
    if b > q:
        return "Connection reset"
    try:
        hmac, B = diffie_hellman(int(A), g, b, p)
        res = jsonify({"hmac": hmac, "B": B, "p": p, "q": q, "g": g})
        res.set_cookie('session', session['id'])
        return res
    except:
        return "Internal error. A was: " + str(A)

f = open("flag.txt", "r")
flag = f.read().strip()
b = bytes_to_long_flag(flag.encode('utf-8'))

if __name__ == "__main__":
    app.run(port=54321)
