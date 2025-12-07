from flask import Flask,

, request, redirect, url_for, render_template_string, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

chat_logs = []

CHAT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P3rf3ctr00t CTF • Global Chat</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Orbitron', 'Courier New', monospace;
            background: #000;
            color: #0f0;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 255, 0, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 0, 0.1) 0%, transparent 20%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(0, 5, 0, 0.95);
            border: 2px solid #0f0;
            border-radius: 8px;
            width: 100%;
            max-width: 750px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
            animation: glow 3s infinite alternate;
        }
        @keyframes glow { from { box-shadow: 0 0 20px rgba(0,255,0,0.5); } to { box-shadow: 0 0 40px rgba(0,255,0,0.8); } }
        .header {
            background: #000;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #0f0;
        }
        .header h1 {
            font-size: 36px;
            font-weight: 900;
            text-shadow: 0 0 10px #0f0;
            letter-spacing: 4px;
        }
        .header .subtitle {
            color: #0a0;
            font-size: 12px;
            letter-spacing: 3px;
            margin-top: 8px;
        }
        .user-badge {
            background: #001a00;
            display: inline-block;
            padding: 6px 14px;
            border: 1px solid #0f0;
            border-radius: 4px;
            margin-top: 10px;
            font-size: 14px;
        }
        .content { padding: 25px; }
        #chat-box {
            background: #000;
            border: 1px dashed #0f0;
            height: 420px;
            overflow-y: auto;
            padding: 15px;
            margin-bottom: 20px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
        }
        #chat-box::-webkit-scrollbar-thumb { background: #0f0; }
        #chat-box::-webkit-scrollbar-track { background: #001a00; }
        .chat-message {
            margin-bottom: 12px;
            animation: type 0.5s steps(30) forwards;
            opacity: 0;
            animation-delay: calc(0.05s * var(--i));
        }
        @keyframes type { from { opacity: 0; } to { opacity: 1; } }
        .chat-username { color: #0ff; text-shadow: 0 0 5px #0ff; font-weight: bold; }
        .chat-text { color: #0f0; }
        .admin-msg {
            color: #f00 !important;
            text-shadow: 0 0 10px #f00;
            font-weight: bold;
            animation: blink 1s infinite;
        }
        @keyframes blink { 50% { opacity: 0.7; } }
        input[type="text"], button {
            background: #000;
            border: 1px solid #0f0;
            color: #0f0;
            padding: 12px 16px;
            font-family: inherit;
            font-size: 14px;
        }
        input[type="text"]:focus, button:hover {
            outline: none;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
        }
        button {
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover { background: #003300; transform: translateY(-2px); }
        .logout-btn { background: #330000; border-color: #f00; color: #f00; margin-top: 10px; width: 100%; }
        .welcome-container { text-align: center; padding: 40px 20px; }
        .welcome-container h2 { font-size: 28px; margin: 20px 0; text-shadow: 0 0 10px #0f0; }
        .flag-hint { color: #060; font-size: 11px; margin-top: 30px; opacity: 0.6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>P3rf3ctr00t CTF</h1>
            <p class="subtitle">> r00tCh4t v1.337</p>
            {% if username %}
                <div class="user-badge">USER: {{ username | e }}</div>
            {% endif %}
        </div>
        <div class="content">
            {% if username %}
                <div id="chat-box">
                    {% if chat_content %}
                        {{ chat_content | safe }}
                    {% else %}
                        <div style="text-align:center; color:#060; margin-top:80px;">
                            <pre style="font-size:18px;">
  .     _ _ _ 
 /_ _ _/_ _ _ _ 
(__(__(__(__(__(
                            </pre>
                            <p>Waiting for root access...</p>
                            <p style="margin-top:30px; color:#030;">Hint: The flag is somewhere in the chat... if you're admin ;)</p>
                        </div>
                    {% endif %}
                </div>
                <form method="POST" action="/send_message">
                    <input type="text" name="message" placeholder="> enter command..." required autofocus>
                    <button type="submit">EXECUTE</button>
                </form>
                <form method="GET" action="/logout">
                    <button type="submit" class="logout-btn">DISCONNECT</button>
                </form>
            {% else %}
                <div class="welcome-container">
                    <h2>WELCOME HACKER</h2>
                    <p>Choose your callsign to enter the matrix</p>
                    <form method="POST" action="/set_username">
                        <input type="text" name="username" placeholder="callsign" required autofocus maxlength="14">
                        <button type="submit">BREACH</button>
                    </form>
                    <div class="flag-hint">
                        Tip: root sometimes spills the beans in the chat...<br>
                        Format: r00t{...}
                    </div>
                </div>
            {% endif %}
        </div>
    </div>
    <script>
        const chatBox = document.getElementById('chat-box');
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
            document.querySelectorAll('.chat-message').forEach((el, i) => {
                el.style.setProperty('--i', i);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    username = session.get('username')
    chat_content = render_template_string('<br>'.join(chat_logs)) if chat_logs else ""
    return render_template_string(CHAT_TEMPLATE, username=username, chat_content=chat_content)

@app.route('/set_username', methods=['GET', 'POST'])
def set_username():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if len(username) > 14:
            return "<h1 style='color:#0f0;background:#000'>ERROR: CALLSIGN TOO LONG</h1>", 400
        if '{' in username and '}' in username:
            return "<h1 style='color:#0f0;background:#000'>NICE TRY ;)</h1>", 400
        session['username'] = username
        return redirect(url_for('home'))
    return render_template_string(CHAT_TEMPLATE, username=None)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('set_username'))
    message = request.form.get('message', '')
    if not message.replace(' ', '').replace('\n', '').isalnum():
        return "<h1 style='color:#f00;background:#000'>INVALID CHARACTERS DETECTED</h1>", 400
    chat_logs.append(f"{session['username']}: {message}")
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('set_username'))

@app.route('/reset', methods=['GET'])
def reset():
    global chat_logs
    chat_logs = []
    session.pop('username', None)
    return "<h1 style='color:#0f0;background:#000'>SYSTEM RESET COMPLETE</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
