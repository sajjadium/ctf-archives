from flask import Flask, render_template, request, redirect, url_for, jsonify
import hashlib
import base64
import json
import time
import random
import hashlib
from Crypto.Util.number import bytes_to_long, isPrime
import math

app = Flask(__name__)

def hash_string_sha256(message):
    message_bytes = message.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message_bytes)
    hashed_message = sha256_hash.digest()

    return int.from_bytes(hashed_message, byteorder='big')

def generate_signature(message, private_key):
    n, d = private_key
    hashed_message = hash_string_sha256(message)
    signature = pow(hashed_message, d, n)
    
    return signature

def verify_signature(msg, public_key, signature):
    initial_hash = hash_string_sha256(msg)
    
    n, e = public_key
    
    recoved_hash = pow(int(signature),e,n)
    
    return initial_hash == recoved_hash

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the user exists
    if username not in users:
        return redirect(url_for('login', reason='unknown_user'))

    # Check if the password is correct
    if password != users[username][0]:
        return redirect(url_for('login', reason='incorrect_password'))
    
    public_key, private_key = generate_key(username)
    
    public_key_users[username] = public_key
    
    signature = generate_signature(str({username : [users[username][1]]}), private_key)
    
    return redirect(url_for('news', token=signature, message=base64.b64encode(str({username : [users[username][1]]}).encode()).decode()))

@app.route('/news', methods=['GET'])
def news():
    signature = request.args.get('token')
    message = base64.b64decode(request.args.get('message')).decode()
    
    message = json.loads(message.replace("'", '"').replace("False", "false").replace("True", "true"))
    
    username = list(message.keys())[0]
    subscribe = list(message.values())[0][0]

    if signature:
        is_sign = verify_signature(str(message), public_key_users[username], signature)
        if is_sign:
            return render_template('news.html', username=username, subscribe=subscribe)

    return redirect(url_for('login', reason='unauthorized'))

@app.route('/login', methods=['GET'])
def show_login():
    # Extract the reason from the query parameters
    reason = request.args.get('reason')

    # Display a pop-up message based on the reason
    if reason == 'unknown_user':
        pop_up_message = "Unknown user. Please check your credentials."
    elif reason == 'incorrect_password':
        pop_up_message = "Incorrect password. Please try again."
    elif reason == 'unauthorized':
        pop_up_message = "Unauthorized access. Please log in."
    else:
        pop_up_message = None

    return render_template('login.html', pop_up_message=pop_up_message)

@app.route('/create_user', methods=['POST'])
def create_user():
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')

    # Check if the username already exists
    if new_username in users:
        return redirect(url_for('login', reason='username_exists'))

    # Add the new user to the dictionary
    users[new_username] = [new_password, False]

    # Display a pop-up message
    pop_up_message = "Thanks for registering! The admin will soon activate your profile if you have subscribed."

    return render_template('login.html', pop_up_message=pop_up_message)

def generate_key(username):
    
	length = lambda x : len(bin(x)[2:])

	s = bytes_to_long(username.encode())

	random.seed(s)

	e = 0x1001
	phi = 0
    
	while math.gcd(phi,e) != 1:
		n = 1
		factors = []

		while length(n) < 2048:
			temp_n = random.getrandbits(48)
			if isPrime(temp_n):
				n *= temp_n
				factors.append(temp_n)
		phi = 1
		for f in factors:
			phi *= (f - 1)

	d = pow(e, -1, phi)

	return (n,e), (n,d)

# A simple dictionary to store user credentials and subscription status
users = {
    'GCC': ['securePassword', False]
}
public_key_users = {}

if __name__ == '__main__':
    app.run(debug=False)
