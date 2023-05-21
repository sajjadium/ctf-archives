from flask import Flask, request, render_template
from fast_jwt import encode, decode
import uuid
import base64

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/apply', methods=['POST'])
def apply():
    token = request.form.get('token')

    public_key = open('publickey.crt', 'br').read()

    reason = ''
    try:
        decoded = decode(token, public_key)
    except Exception as e:
        reason = str(e)
        decoded = None

    fail = decoded is None or 'username' not in decoded or 'admin' not in decoded

    message = 'Test success:' + str(decoded) if not fail else 'Test failed! ' + reason

    if not fail and decoded['admin'] is True:
        return render_template('flag.html')

    return render_template('user.html', message=message)


@app.route('/get_token', methods=['GET'])
def get_token():
    private_key = open('keypair.pem', 'br').read()
    public_key = open('publickey.crt', 'br').read()
    public_key = base64.b64encode(public_key.replace(b'\n', b'')).decode('ascii')
    username = str(uuid.uuid4())
    payload = {'username': username, 'admin': False}
    encoded = encode(payload, private_key, 'RS256', public_key)
    return render_template('token.html', token=encoded)
