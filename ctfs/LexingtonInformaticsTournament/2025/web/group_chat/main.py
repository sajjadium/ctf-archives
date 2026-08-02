from flask import Flask, render_template, render_template_string, request, session, redirect, url_for
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

chat_logs = []  # Store chat messages in memory


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('set_username'))
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Room</title>
</head>
<body>
    <script>
    function check(event) {
        const regex = /^[a-zA-Z0-9]*$/;
        const char = String.fromCharCode(event.keyCode);
        if (!regex.test(char) && event.key !== "Backspace" && event.key !== "Delete") {
            event.preventDefault();
        }
    }
    </script>
    <h2>Chat Room</h2>
    <div id="chat-box">''' + '<br>'.join(chat_logs) + '''
    </div>
    <form action="/send_message" method="POST">
        <input type="text" onkeydown="check(event)" name="message" placeholder="Type a message" required>
        <button type="submit">Send</button>
    </form>
</body>
</html>
'''
    return render_template_string(html)


@app.route('/set_username', methods=['GET', 'POST'])
def set_username():
    if request.method == 'POST':
        if len(request.form['username']) > 1000:
            return redirect(url_for('set_username'))
        if request.form['username'].count('{') and request.form['username'].count('}'):
            return redirect(url_for('set_username'))
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Set Username</title>
</head>
<body>
    <h2>Set Your Username</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Enter username" required>
        <button type="submit">Set Username</button>
    </form>
</body>
</html>
'''
    return render_template_string(html)


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('set_username'))
    msg = request.form['message']
    username = session.get('username', 'Guest')
    if not msg.isalnum():
        return redirect(url_for('index'))
    chat_message = username + ': ' + msg
    chat_logs.append(chat_message)

    return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app, debug=False)
