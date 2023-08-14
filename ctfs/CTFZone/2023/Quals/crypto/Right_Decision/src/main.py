import random
import string
import Crypto.Util.number as number
import numpy as np
import json
import socketserver
import galois
from hashlib import md5

PORT = 31339

with open('params.txt') as f:
    params = json.load(f)

p = params['galois_p']
k = params['k']
n = params['RSA_n']
gf = galois.GF(p,verify=False,primitive_element=2)

with open('votes.txt') as f:
    votes = json.load(f)

with open('flag.txt') as f:
    flag = f.read()

def check_secret(s):
    #check if secret is real phi for public key n
    return pow(2,s,n)==1

def parse_new_vote(data):
    all_votes = votes.copy()
    all_votes.append(json.loads(data))
    
    #check if we have k true votes
    true_votes = sum([v['vote'] for v in all_votes])
    if true_votes<k:
        return 'bad vote!'
    
    #calculate Shamir's shared secret
    matrix = [[ gf(vote['i'])**(k-j-1) for j in range(k)] for vote in all_votes]
    values = [vote['value'] for vote in all_votes]
    matrix = gf(matrix)
    values = gf(values)
    r = np.linalg.solve(matrix,values)
    for_test = int(r[-1])

    # ok, now check that secret is correct
    if check_secret(for_test):
        return flag
    else:
        return 'bad vote!'



class CheckHandler(socketserver.BaseRequestHandler):

    def check_pow(self):
        prefix = ''.join(random.choices(string.ascii_letters,k=10))
        pow_size = 7 # 3.5 byte
        hash_bytes = ''.join(random.choices('abcdef1234567890',k=pow_size))
        self.request.sendall(("Welcome! Please provide proof of work. \nPrefix: "+prefix+"\nTarget hash starts with:"+hash_bytes+'\nEnter: ').encode('utf-8'))
        response = self.request.recv(100).decode('utf-8').strip()
        if md5((prefix+response).encode('utf-8')).hexdigest().startswith(hash_bytes):
            self.request.sendall(b'Proof of work confirmed. Go on!\n\n')
            return True
        else:
            self.request.sendall(b'Proof of work is bad. Bye!')
            return False

    def handle(self):
        if not self.check_pow():
            return 

        self.request.sendall(b'Present your vote: \n')
        data = self.request.recv(10000).strip()
        try:
            resp = parse_new_vote(data)
        except:
            resp = 'bad vote!'
        
        self.request.sendall(resp.encode('utf-8'))

if __name__ == '__main__':
	server = socketserver.TCPServer(('0.0.0.0',PORT),CheckHandler)
	server.serve_forever()
