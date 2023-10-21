import hashlib
import os

def generate_proof_of_work(size,difficulty):
    target = os.urandom(size).hex()
    hash_value = hashlib.sha1(target.encode()).hexdigest()
    return target[difficulty:],hash_value

def check_proof_of_work(prefix,suffix,expected):
    return hashlib.sha1(f'{prefix}{suffix}'.encode()).hexdigest()==expected

def proof():
    POW_SIZE=32
    POW_DIFFICULTY=6
    suff,hs=generate_proof_of_work(POW_SIZE,POW_DIFFICULTY)
    print(f'sha1(prefix+"{suff}")=={hs}')
    pref=input("prefix = ?\n")
    if not check_proof_of_work(pref,suff,hs):
        print("PoW error")
        exit(1)
