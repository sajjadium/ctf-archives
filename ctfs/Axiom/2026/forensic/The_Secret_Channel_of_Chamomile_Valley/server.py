import requests
from flask import Flask, request
import threading
import time
import sys
import random
import os

key_decrypt = random.randint(0, 256)
file_counter = 0
key_encrypt = ""
agents = "Axiom CTF 2026: 1st Edition"
app = Flask(__name__)

my_port = 5000
partner_adress = ""

def encrypt(data, key):
    iv = (((data[1] + 5) ^ (data[0] + 17)) << 16) & 0xff
    key = key ^ iv
    encrypted = []
    for byte in data:
        encrypted.append(byte ^ key ^ iv)
    return encrypted

def decrypt(encrypted_data, key):
    iv = (((encrypted_data[1] + 5) ^ (encrypted_data[0] + 17)) << 16) & 0xff
    key = key ^ iv
    decrypted = []
    for byte in encrypted_data:
        decrypted.append(byte ^ key ^ iv)
    return bytes(decrypted)

def send_data(adress, data):
    try:
        enc_data = bytes(encrypt(data, key_encrypt)) 
        ans = requests.post(
            url=f"http://{adress}/receive",
            data=enc_data,
            headers={'User-Agent': agents},
            timeout=5
        )
        if ans.status_code == 200:
            print("✓ Delivered")
        else:
            print("✗ Network error!")
    except Exception as e:
        print(f"✗ Error: {e}")

@app.route('/receive', methods=['POST'])
def receive_data():
    global file_counter
    enc_data = request.data
    try:
        decrypted = decrypt(enc_data, key_decrypt)
        decrypted.decode()
        print(f"\n>>> {decrypted.decode()}")
        print("You: ", end="", flush=True)
    except Exception:
        os.makedirs("received", exist_ok=True)
        path = f"received/{file_counter}.dat"
        with open(path, "wb") as f:
            f.write(enc_data)
        print(f"\n[Saved binary data to {path}]")
        file_counter += 1
    return {"status": "ok"}, 200

def sender():
    global partner_adress, key_encrypt
    your_name = input("Your name: ")
    partner_adress = input("Partner address (like agent2:5000): ")
    key_encrypt = int(input("Shared encryption key: "))
    
    print(f"\n[Connected to {partner_adress}]\n")
    
    while True:
        try:
            print("You: ", end="", flush=True)
            data = input()
            if data.lower() == 'exit':
                break
            if data:
                msg = f"{your_name}: {data}"
                send_data(partner_adress, msg.encode())
        except KeyboardInterrupt:
            print("\n[Exit]")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    flask_thread = threading.Thread(
        target=lambda: app.run(
            host='0.0.0.0',  
            port=my_port, 
            debug=False, 
            use_reloader=False
        ), 
        daemon=True
    )
    flask_thread.start()
    time.sleep(1)
    sender()