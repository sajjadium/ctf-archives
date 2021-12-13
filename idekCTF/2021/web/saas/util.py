from PIL import Image
import random
import jwt
import string
import os
from imghdr import tests
import subprocess

priv_key = open('keys/private.pem', 'r').read()


def create_token():
    priv_key = open('keys/private.pem', 'r').read()
    token = jwt.encode({"username": f"guest_{random.randint(1,10000)}"}, priv_key, algorithm='RS256', headers={'pubkey': 'public.pem'})
    return token

def verify_token(token):
    try:
        headers = jwt.get_unverified_header(token)
        pub_key_path = headers['pubkey']
        pub_key_path = pub_key_path.replace('..', '') # no traversal!
        pub_key_path = os.path.join(os.getcwd(), os.path.join('keys/', pub_key_path))
        pub_key = open(pub_key_path, 'rb').read()
        if b'BEGIN PUBLIC KEY' not in pub_key:
            return False
        return jwt.decode(token, pub_key, algorithms=['RS256', 'HS256'])
    except:
        return False

def rand_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))

def embed_file(embed_file, cover_file, stegfile, password):
    cmd = subprocess.Popen(['steghide', 'embed', '-ef', embed_file, '-cf', cover_file, '-sf', stegfile, '-p', password]).wait(timeout=.5)

def cleanup():
    for f in os.listdir('uploads/'):
        os.remove(os.path.join('uploads/', f))
    for f in os.listdir('output/'):
        os.remove(os.path.join('output/', f))


