import gmpy2
import json
import random
import requests
import time


BASE = "https://securityisamyth.q.2024.ugractf.ru"
TOKEN = input("Enter token: ")


p, g, y = [int(n, 16) for n in requests.post(f"{BASE}/{TOKEN}/get-parameters").text.split(", ")]

print("Computing, please wait...")
rs = [random.randint(0, p - 2) for _ in range(32)]
cs = [int(gmpy2.powmod(g, r, p)) for r in rs]

choices = eval(requests.post(f"{BASE}/{TOKEN}/announce-cs", data=b"".join(c.to_bytes(16384 // 8) for c in cs)).text)

x = eval(input(f"Please solve {g:x}^x = 0x{y:x} (mod 0x{p:x}) for x: "))
print("Verifying...")
answers = [(x + r) % (p - 1) if choice == 0 else r for r, choice in zip(rs, choices)]
result = requests.post(f"{BASE}/{TOKEN}/answer-choices", data=b"".join(answer.to_bytes(16384 // 8) for answer in answers)).text
print(result)
