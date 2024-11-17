from flask import Flask, request, jsonify
import base64
import hashlib

app = Flask(__name__)

def base64_decode(data):
    try:
        return base64.b64decode(data)
    except Exception:
        return None

def validate_pair(data1, data2):
    decoded1 = base64_decode(data1)
    decoded2 = base64_decode(data2)
    
    if decoded1 is None or decoded2 is None:
        return False
    if b"whale_meowing" not in decoded1 or b"whale_meowing" not in decoded2:
        return False

    md5_1 = hashlib.md5(decoded1).hexdigest()
    md5_2 = hashlib.md5(decoded2).hexdigest()
    return md5_1 == md5_2

@app.route('/check', methods=['POST'])
def check():
    try:
        data = request.get_json()

        if not isinstance(data, list) or not all(isinstance(pair, list) and len(pair) == 2 for pair in data):
            return jsonify({"status": "wrong", "error": "Invalid input format"}), 400

        if len(data) != 100:
            return jsonify({"status": "wrong", "error": "Exactly 100 pairs required"}), 400

        all_inputs = [item for pair in data for item in pair]
        if len(all_inputs) != len(set(all_inputs)):
            return jsonify({"status": "wrong", "error": "Duplicate inputs found"}), 400
        
        for pair in data:
            if not validate_pair(pair[0], pair[1]):
                return jsonify({"status": "wrong"}), 200
        
        return jsonify({"status": "NHNC{FAKE_FLAG}"}), 200

    except Exception as e:
        return jsonify({"status": "wrong", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=31337)