from flask import Flask, request, url_for, session, jsonify
from db import DB, DBException
from functools import wraps
import utils
import os
import jwt

app = Flask(__name__)

app.config['SECRET_KEY'] = utils.random_string(20)
app.config['SHARED_SECRET'] = os.environ.get(
    'SHARED_SECRET', 'segreto_segretissimo_much_segreto')
app.config['PAYURL'] = os.environ.get('PAYURL', 'http://localhost:5050')
app.config['APPURL'] = os.environ.get('APPURL', 'http://localhost:5000')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            print(request.headers["Authorization"])
            token = request.headers["Authorization"]

        if not token:
            return jsonify({
                "error": "Missing token",
            }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

            db = DB()
            current_user = db.get_user_from_id(data['user_id'])

            if current_user is None:
                return jsonify({
                    "error": "Invalid token"
                }), 401

        except Exception as e:
            print(e)
            return jsonify({
                "error": "Exception pazza",
            }), 500

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/user/item')
@token_required
def index_view(current_user):
    db = DB()
    owned_items = db.get_owned_items(current_user.id)
    owned_items = [
        {
            'name' : x.name,
            'content' : x.content
        } for x in owned_items
    ]
    return jsonify({
        'items' : owned_items
    }), 200


@app.route('/api/register', methods=['POST'])
def register_view():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({
            'error' : 'Invalid username or password'
        }), 400

    db = DB()

    if db.register(username, password):
        return jsonify({}), 201

    return jsonify({
        'error' : "Can't register, try again"
    }), 400


@app.route('/api/login', methods=['POST'])
def login_view():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({
            'error' : 'Invalid username or password'
        }), 400

    db = DB()

    user = db.login(username, password)

    if user:
        try:
            token = jwt.encode(
                {"user_id": user.id},
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return jsonify({
                "token": token,
            }), 200
        except Exception as e:
            return jsonify({
                "error": "Bohboh",
            }), 500
        return jsonify({}), 200

    return jsonify({
        'error' : 'Invalid credentials'
    }), 400


@app.route('/api/item', methods = ['GET'])
def list_view():
    db = DB()
    items = db.get_all_items()

    items = [
        {
            'id' : x.id,
            'name' : x.name,
            'cost' : x.cost
        } for x in items
    ]
    
    return jsonify({
        'items' : items
    }), 200


@app.route('/api/buy', methods=['POST'])
@token_required
def shop_view(current_user):
    item_id = request.form.get('item_id')

    db = DB()
    item = db.get_item_from_id(item_id)

    if not item:
        return jsonify({
            'error' : 'Invalid item!'
        }), 400

    tx = db.make_transaction(current_user.id, item.id)

    data = {
        "url": f"{app.config['APPURL']}/checkout",
        "amount": item.cost,
        "transaction_id": tx.id,
    }

    token = jwt.encode(
        data, app.config['SHARED_SECRET'], algorithm="HS256")

    return jsonify({
        'url' : f'{app.config["PAYURL"]}/pay?token={token}&amount={item.cost}&user={current_user.username}'
    }), 200


@app.route('/api/checkout_transaction', methods=['POST'])
@token_required
def checkout(current_user):
    token = request.form.get('token')

    if not token:
        return jsonify({
            'error' : 'Invalid transaction'
        }), 400

    try:
        transaction_id, status = utils.parse_token(token, app.config['SHARED_SECRET'])
    except jwt.exceptions.DecodeError:
        return jsonify({
            'error' : 'Invalid transaction, error in token parsing'
        }), 400

    if status:
        db = DB()
        db.checkout_transaction(transaction_id)
    else:
        return jsonify({
            'error' : 'Error during the checkout'
        }), 400

    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
