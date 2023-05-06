import requests

import hashlib
import uuid
import binascii
import os
import sys

def generate():
    return uuid.uuid4().hex[:4], uuid.uuid4().hex[:4]

def verify(prefix, suffix, answer, difficulty=6):
    hash = hashlib.sha256(prefix.encode() + answer.encode() + suffix.encode()).hexdigest()
    return hash.endswith("0"*difficulty)

def solve(prefix, suffix, difficulty):
    while True:
        test = binascii.hexlify(os.urandom(4)).decode()
        if verify(prefix, suffix, test, difficulty):
            return test


s = requests.Session()
host = "https://fbg.rars.win/"

data = s.get(host + "pow").json()
print("Solving POW")
solution = solve(data['pref'], data['suff'], 5)
print(f"Solved: {solution}")
s.post(host + "pow", json={"answer": solution})

name = "" # change this
link = "" # change this
r = s.get(host + f"admin?title={name}&link={link}")
print(r.text)