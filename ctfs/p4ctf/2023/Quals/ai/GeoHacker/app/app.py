# app.py
from flask import Flask, render_template, request, jsonify
import hashlib
import math
import time
import sqlite3
import secrets
from haversine import haversine
from geotask.eval_one import load_model, eval_one, eval_multi
from geotask.downloader.streetview import panoids
from flag import flag_s

app = Flask(__name__)

model = load_model("./geotask/2023-04-17-geoguessr-20.pth")

difficulty = 5
def init_db():
    conn = sqlite3.connect('proofs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS used_proofs (proof TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS generated_prefixes (prefix TEXT UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

def store_generated_prefix(prefix):
    conn = sqlite3.connect('proofs.db')
    c = conn.cursor()
    c.execute("INSERT INTO generated_prefixes (prefix) VALUES (?)", (prefix,))
    conn.commit()
    conn.close()

def is_prefix_generated(prefix):
    conn = sqlite3.connect('proofs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM generated_prefixes WHERE prefix = ?", (prefix,))
    result = c.fetchone()
    conn.close()
    return result is not None

def store_used_proof(proof):
    conn = sqlite3.connect('proofs.db')
    c = conn.cursor()
    c.execute("INSERT INTO used_proofs (proof) VALUES (?)", (proof,))
    conn.commit()
    conn.close()

def is_proof_used(proof):
    conn = sqlite3.connect('proofs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM used_proofs WHERE proof = ?", (proof,))
    result = c.fetchone()
    conn.close()
    return result is not None

def check_proof(prefix, nonce):
    guess = f'{prefix}{nonce}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "0" * difficulty


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prefix')
def get_prefix():
    prefix = secrets.token_hex(8)
    store_generated_prefix(prefix)
    return jsonify({'prefix': prefix, "difficulty": difficulty})

# app.py
@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    locations = data.get('locations')
    nonce = data.get('nonce')
    prefix = data.get('prefix')
    proof_string = f'{prefix}{nonce}'

    if not is_prefix_generated(prefix):
        return jsonify({'status': 'failed', 'reason': 'invalid prefix'}), 400

    if is_proof_used(proof_string):
        return jsonify({'status': 'failed', 'reason': 'invalid proof'}), 400

    if not check_proof(prefix, nonce):
        return jsonify({'status': 'failed', 'reason': 'invalid proof'}), 400

    store_used_proof(proof_string)

    preds = []
    score = 0

    for i in range(len(locations)):
        for j in range(len(locations)):
            if i == j:
                continue
            lat1, lon1 = locations[i]['lat'], locations[i]['lng']
            lat2, lon2 = locations[j]['lat'], locations[j]['lng']
            dist = haversine((lat1, lon1), (lat2, lon2))
            if dist <= 50:
                return jsonify({'status': 'failed', 'reason': 'points too close'}), 400

    if len(locations) != 5:
        return jsonify({'status': 'failed', 'reason': 'must have 5 guesses'}), 400
    pns = []
    for location in locations:
        try:
            pns.append(panoids(location["lat"], location["lng"])[0]['panoid'])
        except Exception as e:
            print(location)
            return jsonify({'status': 'failed', 'reason': 'no streetview in one of those points'}), 400
    score = 0
    scores = []
    preds = eval_multi(model, panoids=pns)
    for location, pred in zip(locations, preds):
        print(location, pred)
        x = haversine(pred, (location["lat"], location["lng"]))

        tmp_score = int(5000*(math.e**(-x/2000)))
        scores.append((location, tmp_score))
        score += tmp_score

    if score < 1000:
        return jsonify({'status': 'success', 'flag': flag_s + f' score {score}'})
    else:
        return jsonify({'status': 'failed', 'reason': f'my brainz know where those are! your score was {score}, {scores}, try going below 1000'}), 400

if __name__ == '__main__':
    app.run(debug=True)

