from flask import Flask, render_template, request, redirect, url_for, session, make_response
from werkzeug.security import check_password_hash
import os
import time
import base64
import subprocess


app = Flask(__name__)
app.secret_key = os.urandom(24)

f=open('flag.txt')
flag=f.read().rstrip('\n')

def load_users():
    users = {}
    if os.path.exists('databases/users.txt'):
        with open('databases/users.txt', 'r') as f:
            for line in f:
                username, password_hash, rights = line.strip().split(';')
                users[username] = {'password_hash': password_hash, 'rights': rights}
    return users

def save_users(users):
    with open('databases/users.txt', 'w') as f:
        for username, data in users.items():
            f.write(f"{username};{data['password_hash']};{data['rights']}\n")

def load_chats(user1, user2):
    chats = []
    if user1 == "KingMonkey":
        save_chat("KingMonkey", user2, flag)
    if user2 == "KingMonkey":
        save_chat("KingMonkey", user1, flag)
    filename = f"databases/chats/{min(user1, user2)}_{max(user1, user2)}.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                try:
                    from_user, to_user, date, message = line.strip().split(';')
                except:
                    continue
                if (from_user == user1 and to_user == user2) or (from_user == user2 and to_user == user1):
                    chats.append({'from': from_user, 'to': to_user, 'date': date, 'message': message})
    return chats


def save_chat(from_user, to_user, message):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    filename = f"databases/chats/{min(from_user, to_user)}_{max(from_user, to_user)}.txt"
    print(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)  #
    with open(filename, 'a') as f:
        f.write(f"{from_user};{to_user};{date};{message.replace(';','')}\n")


def get_active_conversations(user):
    active_conversations = []
    for filename in os.listdir('databases/chats'):
        if filename.startswith(user):
            other_user = filename.replace(f"{user}_", "").replace(".txt", "")
            active_conversations.append(other_user)
        if filename.endswith(f"_{user}.txt"):
            other_user = filename.replace(f"_{user}.txt", "")
            active_conversations.append(other_user)
    return active_conversations



@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('news'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and check_password_hash(users[username]['password_hash'], password):
            rights = base64.b64encode(users[username]['rights'].encode('utf-8')).decode('utf-8')
            result = subprocess.run([f"{os.getcwd()}/superadminverificator", "--operation", "0", "--data", rights], capture_output=True)
            specs = result.stdout.decode('utf-8').rstrip('\n')
            print(specs)
            resp = make_response(redirect(url_for('news')))
            # We should as this in session 
            resp.set_cookie('rights', rights)
            resp.set_cookie('specs', specs)
            session['username'] = username
            return resp 
        else:
            return "Invalid credentials!", 401

    return render_template('login.html')

@app.route('/news')
def news():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('news.html', username=session['username'])

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_rights = request.cookies.get('rights')
    try:
        rights = base64.b64decode(user_rights)
    except Exception as e:
        rights = b""
    specs = request.cookies.get('specs')
    if user_rights is None or specs is None:
        return redirect(url_for('news'))

    
    result = subprocess.run([f"{os.getcwd()}/superadminverificator", "--operation", "1", "--data", f"{user_rights}", "--value", f"{specs}"], capture_output=True)

    users = load_users()
    user_list = []
    if result.returncode == 0:
        if rights.endswith(b"_super"):
            user_list += [username for username, data in users.items() ]
        elif rights.endswith(b"admin"):
            user_list = [username for username, data in users.items() if data['rights'] in ['admin', 'member']]
        else:
            user_list = [username for username, data in users.items() if data['rights'] == 'member']

    else:
        return redirect(url_for('news'))

    if request.method == 'POST':
        to_user = request.form['to_user']
        message = request.form['message']
        if to_user in user_list:
            save_chat(session['username'], to_user, message)

    active_conversations = get_active_conversations(session['username'])
    to_user = request.args.get('to_user')
    if to_user:
        chats = load_chats(session['username'], to_user)
    else:
        chats = [] 

    return render_template('chat.html', chats=chats, users=user_list, active_conversations=active_conversations)


if __name__ == '__main__':
    app.run(debug=False)
