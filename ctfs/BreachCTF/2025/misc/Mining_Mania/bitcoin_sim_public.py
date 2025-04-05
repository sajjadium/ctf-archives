import hashlib
import time
import struct
import json
import threading
from typing import List
from flask import Flask, request, jsonify

def little_endian(hex_str, length):
    """Convert a hex string to little-endian format with a fixed length."""
    return bytes.fromhex(hex_str)[::-1].hex().ljust(length * 2, '0')

class Block:
    def __init__(self, index, prev_hash, merkle_root, timestamp, bits, nonce):
        self.index = index
        self.version = 1  
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits  
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        version = struct.pack('<I', self.version).hex()  # 4 bytes, little-endian
        prev_block = little_endian(self.prev_hash, 32)  # 32 bytes, little-endian
        merkle_root = little_endian(self.merkle_root, 32)  # 32 bytes, little-endian
        timestamp = struct.pack('<I', self.timestamp).hex()  # 4 bytes, little-endian
        bits = little_endian(self.bits, 4)  # 4 bytes, little-endian
        nonce = struct.pack('<I', self.nonce).hex()  # 4 bytes, little-endian
        
        # Concatenate block header fields
        block_header_hex = version + prev_block + merkle_root + timestamp + bits + nonce
        block_header_bin = bytes.fromhex(block_header_hex)
        
        # Perform double SHA-256
        hash1 = hashlib.sha256(block_header_bin).digest()
        hash2 = hashlib.sha256(hash1).digest()
        
        # Convert final hash to little-endian
        block_hash = hash2[::-1].hex()
        return block_hash

    def to_dict(self):
        return {
            "index": self.index,
            "hash": self.hash,
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "bits": self.bits,
            "nonce": self.nonce,
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            prev_hash="0" * 64,
            merkle_root="4bf5122e388ed8b9231b1ba9276b71b7",
            timestamp=int(time.time()),
            bits="1d00ffff",
            nonce=0,
        )
        self.chain.append(genesis_block)

    def add_block(self, merkle_root, nonce):
        prev_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            prev_hash=prev_block.hash,
            merkle_root=merkle_root,
            timestamp=int(time.time()),
            bits="1d00ffff",
            nonce=nonce,
        )
        self.chain.append(new_block)

    def validate_block(self, prev_hash, merkle_root, timestamp, bits, nonce):
        temp_block = Block(
            index=len(self.chain),
            prev_hash=prev_hash,
            merkle_root=merkle_root,
            timestamp=timestamp,
            bits=bits,
            nonce=nonce,
        )
        return temp_block.hash.startswith("0000000")  
        

    def get_chain(self):
        return [block.to_dict() for block in self.chain]

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.json
    blockchain.add_block(data["merkle_root"], data["nonce"])
    return jsonify({"message": "Block added", "hash": blockchain.chain[-1].hash})

@app.route("/validate_block", methods=["POST"])
def validate_block():
    data = request.json
    is_valid = blockchain.validate_block(
        data["prev_hash"], data["merkle_root"], data["timestamp"], data["bits"], data["nonce"]
    )

    if not is_valid:
        return jsonify({"valid": is_valid, "message": "Invalid Block Try Again"})
    
    else:
        return jsonify({"valid": is_valid, "message": "Congratulations! You mined a valid block. Here's your reward : [REDACTED]"})



@app.route("/get_chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain.get_chain())

def run_server():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    try:
        threading.Thread(target=run_server, daemon=True).start()
        print("Blockchain simulation is running...")
        while True:
            time.sleep(10)  # Keep the process alive
    except:
        print("Something went wrong. Exiting...")
