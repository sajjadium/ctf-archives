# imports
from flask import Flask, session, request, redirect
import secrets, html


# initialize flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
FLAG = open("flag.txt", "r").read()
SECRET = open("secret.txt", "r").read()
users = [{'username':'admin','password':SECRET}] # NEVER DO THIS IN PRODUCTION fyi
notes = [{
    "note":FLAG,
    "user":"admin",
    "id":"00000000000000000000000000000000",
    "shared":[]
}]
csrf_tokens = []


@app.route('/', methods=['GET'])
def index():
    if 'username' not in session:
        return redirect('/login')
    return f'''
    <h1>Home</h1>
    <p>Welcome {html.escape(session['username'],quote=True)}!</p>
    <a href="/notes"><h3>View notes</h3></a>
    <a href="/logout"><h3>Logout</h3></a>
    '''

@app.route('/notes', methods=['GET'])
def view_notes():
    if 'username' not in session:
        return redirect('/login')
    
    user_notes = []
    for note in notes:
        if note['user'] == session['username']:
            user_notes.append(note)
    
    page = "<h1>Notes</h1>"
    for note in user_notes:
        page += f"<p>{html.escape(note['note'],quote=True)}</p>"
        page += f"<p>{html.escape(note['id'],quote=True)}</p>"

    shared_notes = []
    for note in notes:
        if session['username'] in note['shared']:
            shared_notes.append(note)

    page += "<h1>Shared Notes</h1>"
    for note in shared_notes:
        page += f"<p>{html.escape(note['note'],quote=True)}</p>"
        page += f"<p>{html.escape(note['id'],quote=True)}</p>"

    page += '''
        <a href="/create"><h3>Create note</h3></a>
        <a href="/share"><h3>Share note</h3></a>
        <a href="/logout"><h3>Logout</h3></a>
    '''

    return page


@app.route('/create', methods=['GET', 'POST'])
def create():
    global notes
    
    if len(notes) > 200:
        notes = []

    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        if 'note' not in request.form:
            return 'note cannot be empty'
        
        if not isinstance(request.form['note'], str):
            return 'note must be a string'
        
        if len(request.form['note']) > 100:
            return 'note size is max 100'
        
        notes.append({"note":request.form['note'],"user":session['username'],"id":secrets.token_hex(16),"shared":[]})
        return redirect('/notes')

    return '''
        <h1>Create note</h1>
        <form method="post">
            <p><label for="note">Note Description</label>
            <input type=text name=note>
            <p><input type=submit value=Create>
        </form>

        <a href="/notes"><h3>View notes</h3></a>
    '''

@app.route('/share', methods=['GET', 'POST'])
def share():
    global csrf_tokens
    
    if len(csrf_tokens) > 200:
        csrf_tokens = []

    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        if 'note_id' not in request.form or 'user' not in request.form or 'csrf_token' not in request.form:
            return 'note_id cannot be empty'
        
        if not isinstance(request.form['note_id'], str) or not isinstance(request.form['user'], str) or not isinstance(request.form['csrf_token'], str):
            return 'All parameters must be a string'
        
        if request.form['csrf_token'] not in csrf_tokens:
            return 'CSRF token is invalid'
        
        if len(request.form['note_id']) != 32:
            return 'note_id must be 32 characters'
        
        note_exists = False
        for note in notes:
            if note['id'] == request.form['note_id']:
                note_exists = True
                break
        
        if not note_exists:
            return 'note_id is invalid'
        
        user_exists = False
        for user in users:
            if user['username'] == request.form['user']:
                user_exists = True
                break
        
        if not user_exists:
            return 'User does not exist'
        
        for note in notes:
            if note['id'] == request.form['note_id'] and note['user'] == session['username']:
                note['shared'].append(request.form['user'])
                return redirect('/notes')
            
        return 'You don\'t own this note'
    
    token = secrets.token_hex(32)
    csrf_tokens.append(token)

    return f'''
        <h1>Share note</h1>
        <form method="post">
            <p><label for="note_id">Note ID</label>
            <input type=text name=note_id>
            <p><label for="user">User</label>
            <input type=text name=user>
            <p><input type=submit value=Share>
            <input type=hidden name=csrf_token value={token}>
        </form>

        <a href="/notes"><h3>View notes</h3></a>
    ''' 
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            return 'Username and password cannot be empty'
        
        if not isinstance(request.form['username'], str) or not isinstance(request.form['password'], str):
            return 'Username and password must be strings'    
        
        if (len(request.form['username']) < 9 or len(request.form['password']) < 9) and request.form['username'] != 'admin':
            return 'Username and password must be at least 9 characters'
        
        for user_obj in users:
            if user_obj['username'] == request.form['username'] and user_obj['password'] == request.form['password']:
                session['username'] = request.form['username']
                return redirect('/')
            
        return 'Incorrect username or password'
    return '''
    <h1>Login</h1>
        <form method="post">
            <p><label for="username">Username</label>
            <input id="username" type=text name=username>
            <p><label for="password">Password</label>
            <input id="password" type=text name=password>
            <p><input id="formsubmit" type=submit value=Login>
        </form>

        <a href="/register"><h3>Register here</h3></a>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    global users
    
    if len(users) >= 150:
        users = []


    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            return 'Username and password cannot be empty'
        
        if not isinstance(request.form['username'], str) or not isinstance(request.form['password'], str):
            return 'Username and password must be strings'

        if len(request.form['username']) < 9 or len(request.form['password']) < 9:
            return 'Username and password must be at least 9 characters'

        for user_obj in users:
            if user_obj['username'] == request.form['username']:
                return 'Username already taken'
        
        users.append({"username":request.form['username'],"password":request.form['username']})
        return redirect('/login')
    
    return '''
        <h1>Register</h1>
        <form method="post">
            <p><label for="username">Username</label>
            <input type=text name=username>
            <p><label for="password">Password</label>
            <input type=text name=password>
            <p><input type=submit value=Register>
        </form>

        <a href="/login"><h3>Login here</h3></a>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True)