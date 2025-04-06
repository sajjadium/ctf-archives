import requests
import hashlib
import string
import random

POW_URL = "http://138.199.236.43:5000/pow_challenge"
SPAWN_URL = "http://138.199.236.43:5000/spawn"

def solve_challenge(challenge, difficulty):
    target_nibbles = difficulty // 4
    required_prefix = "0" * target_nibbles

    attempts = 0
    while True:
        nonce_candidate = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        digest = hashlib.sha256((challenge + nonce_candidate).encode()).hexdigest()
        attempts += 1

        if digest.startswith(required_prefix):
            #print(f"[+] Found valid nonce after {attempts} attempts: {nonce_candidate}")
            return nonce_candidate

# solve pow chall and output intance info
def spawn_instance():
    resp = requests.get(POW_URL)
    if resp.status_code != 200:
        #print("Failed to fetch challenge:", resp.text)
        return
    
    data = resp.json()
    challenge = data["challenge"]
    difficulty = data["difficulty"]
    #print("Received challenge:", challenge, "with difficulty:", difficulty)

    nonce = solve_challenge(challenge, difficulty)

    spawn_resp = requests.post(SPAWN_URL, json={
        "challenge": challenge,
        "nonce": nonce
    })

    return spawn_resp.json()

if __name__ == "__main__":
    spawn_instance()

