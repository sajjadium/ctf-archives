import numpy as np
import requests
from binascii import hexlify

url = "http://puzzle.donjon-ctf.io:7000"

def send(dat):
    data = hexlify(bytes(dat, 'utf8')).decode()
    cmd = {'cmd' : 'send', 'data': data }
    x = requests.post(url, json = cmd)
    return x.json()

if __name__ == "__main__":
    print(send("0\n1\n")["message"])
