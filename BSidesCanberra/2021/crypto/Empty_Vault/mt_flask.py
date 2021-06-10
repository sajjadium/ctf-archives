from flask import Flask,render_template, request
app = Flask(__name__)


'''
"What is identity? It is the difference between us. Difference is experienced in the mind, yet the Buddha said this mind creates the world, that this world only exists in the mind and nowhere else."
'''

from hashlib import sha256
import os
from binascii import * 
from flag import flag

class MerkleTree(object): 
    def __init__(self):
        self.leaves = list()
        self.levels = None
        self.is_ready = False

    def add_leaf(self, value):         
        self.leaves.append(sha256(value).digest())

    def _calculate_next_level(self):
        solo_leave = None
        N = len(self.levels[0])  # number of leaves on the level
        if N % 2 == 1:  # if odd number of leaves on the level
            solo_leave = self.levels[0][-1]
            N -= 1

        new_level = []
        for l, r in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):
            new_level.append(sha256(l+r).digest())
        if solo_leave is not None:
            new_level.append(solo_leave)
        self.levels = [new_level, ] + self.levels  # prepend new level

    def make_tree(self):
        self.is_ready = False
        if len(self.leaves) > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self._calculate_next_level()
        self.is_ready = True

    def get_merkle_root(self):
        if self.is_ready:
            if self.levels is not None:
                return self.levels[0][0]
            else:
                return None
        else:
            return None

def hashPassword(p):
    mt = MerkleTree()
    for c in p: 
        mt.add_leaf(c)
    mt.make_tree()
    return hexlify(mt.get_merkle_root())

def generateRandomPassword(length):
    p = os.urandom(length)
    return hexlify(p)

def splitPassword(p, isString=True):
    if isString:
        return ",".join([c for c in p]).split(",")
    else:
        return b",".join([chr(c).encode() for c in p]).split(b",")

def validatePassword(user_password, password_hashes, denyList=[], debug=False):    
    try:
        joined_password = unhexlify("".join(user_password.split(",")))
    except Exception as e: 
        raise Exception("ERROR: Formatting error. Exiting")
        
    if joined_password in denyList: 
        raise Exception("Nice try, but that password is not allowed...")
    
    split_password = [unhexlify(c) for c in user_password.split(",")]
    user_password_hash = hashPassword(split_password)

    if debug: 
        print("user_password entered: [", user_password, "]")
        print("hashes", password_hashes)
        print("deny list", denyList)
        print("hash", user_password_hash)

    if (user_password_hash in password_hashes): 
        return True

    return False

test_password = b"SuperSecretPassword"
test_password_list = splitPassword(test_password, isString=False)
test_password_hash = hashPassword(test_password_list)
password_hashes = [test_password_hash]

for i in range(0,9):
    new_password = generateRandomPassword(32)
    new_password_list = splitPassword(new_password, isString=False)
    new_password_hash = hashPassword(new_password_list)
    password_hashes.append(new_password_hash)

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/auth', methods=['GET'])
def do_auth():
    TP = request.args.get('transformed','')
    P = request.args.get('password','').encode()
    
    if P == test_password:
        return 'Nice try, but that password is not allowed :P'

    try:
        res = validatePassword(TP, password_hashes, denyList=[test_password])
    except Exception as e: 
        return str(e)    

    if res:
        return 'Authed! Here is your flag: '+flag
    else:
        return 'Wrong Password'




