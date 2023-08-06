from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
from os import  urandom
from random import SystemRandom
from sympy import GF
from sympy.polys.matrices import DomainMatrix
import json
from hashlib import md5

random=SystemRandom()
shuffle=random.shuffle
randint=random.randint
randrange=random.randrange
uniform = lambda: randrange(257//2) - 257//2
P=GF(257)


secret=open("Secret.txt",'rb').read()
assert len(secret)==16
flag=open("flag.txt","rb").read()



def encrypt_flag(secret):
    key = hashlib.sha256(secret).digest()[-16:]
    iv = urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc_flag=cipher.encrypt(pad(flag,16))
    return json.dumps({"encrypted_flag":enc_flag.hex(),"IV":iv.hex()})


def get_hint(vec,mat):
    res=(Pub_matrix*vec).to_Matrix()
    res=[int(res[i,0])%257 for i in range(16)]
    shuffle(res)
    return json.dumps({"hint":[i for i in res]})


def get_secret(secret,Secret_matrix):
    secret_vetor=DomainMatrix([[P(int(i))] for i in secret],(16,1),P)
    public_vector=(Secret_matrix*secret_vetor).to_Matrix()
    return json.dumps({"secret":[int(public_vector[i,0]) for i in range(16)]})


while True:
    g=randint(2,257)
    print(json.dumps({"G":int(g)}))
    Secret_matrix=[[uniform() for i in range(16)] for  j in range(16)]
    Pub_matrix=DomainMatrix([[P((pow(g,randint(2,256),257))*i) for i in j] for j in Secret_matrix],(16,16),P)
    Secret_matrix=DomainMatrix(Secret_matrix,(16,16),P) # to make it easier for you <3
    while True:
        try:
            choice=json.loads(input("Choose an option\n"))
            if("option" not in choice):
                print("You need to choose an option")
            elif choice["option"]=="get_flag":
                print(encrypt_flag(secret))
            elif(choice["option"]=="get_hint") and "vector" in choice:
                assert len(choice["vector"])==16
                vec=[[P(int(i))] for i in choice["vector"]]
                input_vector=DomainMatrix(vec,(16,1),P)
                print(get_hint(input_vector,Pub_matrix))
            elif choice["option"]=="get_secret":
                    print(get_secret(secret,Secret_matrix))
            elif choice["option"]=="reset_connection":
                g=randint(2,257)
                print(json.dumps({"G":int(g)}))
                Secret_matrix=[[uniform() for i in range(16)] for  j in range(16)]
                Pub_matrix=DomainMatrix([[P((pow(g,randint(2,256),257))*i) for i in j] for j in Secret_matrix],(16,16),P)
                Secret_matrix=DomainMatrix(Secret_matrix,(16,16),P)
            else:
                print("Nothing that we have Right now ")
        except:
            print("dont try something stupid")
            exit(1)
            break
