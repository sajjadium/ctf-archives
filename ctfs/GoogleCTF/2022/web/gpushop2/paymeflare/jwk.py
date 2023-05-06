import requests
import json
import base64
from Crypto.PublicKey import RSA

res = requests.get('https://www.googleapis.com/oauth2/v3/certs')

keys = json.loads(res.content).get('keys')

for k in keys:
    n = k['n']
    e = k['e']
    
    n = base64.urlsafe_b64decode(n + '==')
    e = base64.urlsafe_b64decode(e + '==')
    
    pub = RSA.construct((int.from_bytes(n, 'big'), int.from_bytes(e, 'big')))
    pem = pub.exportKey()
    open(k['kid'] + '.pem', 'wb').write(pem)
