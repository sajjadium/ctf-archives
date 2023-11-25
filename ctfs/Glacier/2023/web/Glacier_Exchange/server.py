from flask import Flask, render_template, request, send_from_directory, jsonify, session
from flask_restful import Api
from src.coin_api import get_coin_price_from_api
from src.wallet import Wallet
import os
import secrets

app = Flask(__name__)
api = Api(app)

app.secret_key = os.urandom(64)

wallets = {}
def get_wallet_from_session():
    if "id" not in session:
        session["id"] = make_token()
    if session["id"] not in wallets:
        wallets[session["id"]] = Wallet()
    return wallets[session["id"]]

def make_token():
    return secrets.token_urlsafe(16)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "index.html",
    )

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('assets', path)

@app.route('/api/data/fetch/<path:coin>')
def fetch(coin: str):
    data = get_coin_price_from_api(coin)
    return jsonify(data)

@app.route('/api/wallet/transaction', methods=['POST'])
def transaction():
    payload = request.json
    status = 0
    if "sourceCoin" in payload and "targetCoin" in payload and "balance" in payload:
        wallet = get_wallet_from_session()
        status = wallet.transaction(payload["sourceCoin"], payload["targetCoin"], float(payload["balance"]))
    return jsonify({
        "result": status
    })

@app.route("/api/wallet/join_glacier_club", methods=["POST"])
def join_glacier_club():
    wallet = get_wallet_from_session()
    clubToken = False
    inClub = wallet.inGlacierClub()
    if inClub:
        f = open("/flag.txt")
        clubToken = f.read()
        f.close()
    return {
        "inClub": inClub,
        "clubToken": clubToken
    }

@app.route('/api/wallet/balances')
def get_balance():
    wallet = get_wallet_from_session()
    balances = wallet.getBalances()
    user_balances = []
    for name in balances:
        user_balances.append({
            "name": name,
            "value": balances[name]
        })
    return user_balances

@app.route('/api/fetch_coins')
def fetch_coins():
    return jsonify([
                {
                    "name": 'cashout',
                    "value": 'Cashout Account',
                    "short": 'CA'
                },
                {
                    "name": 'glaciercoin',
                    "value": 'GlacierCoin',
                    "short": 'GC'
                },
                {
                    "name": 'ascoin',
                    "value": 'AsCoin',
                    "short": 'AC'
                },
                {
                    "name": 'doge',
                    "value": 'Doge',
                    "short": 'DO'
                },
                {
                    "name": 'gamestock',
                    "value": 'Gamestock',
                    "short": 'GS'
                },
                {
                    "name": 'ycmi',
                    "value": 'Yeti Clubs Manufacturing Inc.',
                    "short": 'YC'
                },
                {
                    "name": 'smtl',
                    "value": 'Synthetic Mammoth Tusks LLC',
                    "short": 'ST'
                },
            ])



if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )
