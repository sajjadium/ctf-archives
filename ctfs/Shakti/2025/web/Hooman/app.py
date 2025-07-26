from flask import Flask, request, redirect, render_template, make_response
import jwt

app = Flask(__name__)
SECRET_KEY = 'Youcanneverhavethis' 
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None  
    if request.method == 'POST':
        data = request.json if request.is_json else request.form
        username = data.get('username')
        if not username:
            error = 'Username required'
            return render_template('login.html', error=error)

        token = jwt.encode({'username': username, 'are_you_hooman': False}, SECRET_KEY, algorithm='HS256')
        resp = make_response(redirect('/login'))
        resp.set_cookie('token', token)
        return resp

    else:
        token = request.cookies.get('token')
        if token:
            try:
                decoded = jwt.decode(token, key=None,options={"verify_signature": False}) 
                if decoded.get('are_you_hooman'):
                    return redirect('/hooman')
                error = "Nah, you ain't hooman T^T"
            except jwt.InvalidTokenError:
                error = "Invalid token"

        return render_template('login.html', error=error)

@app.route('/hooman')
def hooman():
    token = request.cookies.get('token')
    if not token:
        return 'No token provided', 401
    try:
        decoded = jwt.decode(token, key=None,options={"verify_signature": False})
        if decoded.get('are_you_hooman'):
            return '''
<html>
  <head><title>Hooman</title></head>
  <body style="background-color: #333; color: #f0f0f0; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh;">
    <h1>Hiii hoomann a message for ya! shaktictf{f4k3_fl4g}</h1>
  </body>
</html>
'''

        return 'Nah, you ain\'t hooman T^T', 401
    except jwt.InvalidTokenError:
        return 'Invalid token', 401

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)