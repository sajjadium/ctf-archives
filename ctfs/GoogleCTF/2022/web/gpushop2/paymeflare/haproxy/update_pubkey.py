import requests
import base64
import time
from Cryptodome.PublicKey import RSA

OAUTH2_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
OAUTH_PUBKEY_PATH = "/tmp/haproxy/oauth_pubkey.pem"

def gen_pubkey(k):
    n = k['n']
    e = k['e']
    
    n = base64.urlsafe_b64decode(n + '==')
    e = base64.urlsafe_b64decode(e + '==')
    
    pub = RSA.construct((int.from_bytes(n, 'big'), int.from_bytes(e, 'big')))
    pem = pub.exportKey()
    return pem.decode()    


pubkey = open(OAUTH_PUBKEY_PATH).read()
used_keys = set()

res = requests.get(OAUTH2_CERTS_URL).json()
for k in res['keys']:
    used_keys.add(k['kid'])


while True:
    res = requests.get(OAUTH2_CERTS_URL).json()
    for k in res['keys']:
        if k['kid'] not in used_keys:
            print('Updating key', k['kid'])
            used_keys.add(k['kid'])
            pem = gen_pubkey(k)
            open(OAUTH_PUBKEY_PATH, 'wb').write(pem)
            break
    time.sleep(60)
