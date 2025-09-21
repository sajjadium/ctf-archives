import socket, os, time, random, binascii,requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

def get_random() -> bytes:
    channels = [
        "1416908413375479891",
        "1417154025371209852",
    ]
    headers = {
        "Authorization": f"Bot {os.getenv('TOKEN')}",
    }

    all_data = []

    for channel_id in channels:
        url = f"https://proxy-gamma-steel-32.vercel.app/api/proxy/channels/{channel_id}/messages?limit=10"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        messages = response.json()

        for msg in messages:
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            all_data.append(f"{content}{timestamp}")

    concatenated = "".join(all_data).encode("utf-8")
    return concatenated

def encrypt(data: bytes, key: bytes) -> str:
    digest = SHA256.new()
    digest.update(key)
    aes_key = digest.digest()

    iv = get_random_bytes(16)

    padded_data = pad(data, AES.block_size)

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_data)

    return base64.b64encode(iv + ciphertext).decode()


def handle_client(c, flag):
    seed = get_random()
    print(seed, flush=True)
    encrypted_flag = encrypt(flag, seed)
    out = {
        "encrypted": encrypted_flag
    }
    c.sendall((str(out) + "\n").encode())

def main():
    flag=os.environ.get("FLAG","you ran this locally, duh").encode()
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0",5000))
    s.listen(64)
    while True:
        c,a=s.accept()
        try:
            handle_client(c, flag)
        finally:
            c.close()

if __name__=="__main__":
    main()
