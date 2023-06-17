from Crypto.Util.number import long_to_bytes ,getPrime
from random import randint,shuffle
import json
from banner import banner

class LCG:
    def __init__(self,m, seed):
        self.a = randint(1,m)
        self.b = randint(1,m)
        self.m = m
        self.state = seed
        self.refresh()

    def refresh(self):
        self.state = (self.get_random_bits()*self.get_random_bits())%self.m

    def next_state(self):
        self.state = (self.a * self.state + self.b) % self.m

    def get_random_bits(self):
        self.next_state()
        return (self.state)>>100

    def encrypt(self,msg):
        return long_to_bytes(self.get_random_bits()^int(msg,16)).hex()

banner()

m=8232312959811687665793375850697161475128245885498087244865661043365300427355910967177802992671927606112967162365226385902985055038600150891334303906988843
seed=randint(1,m)
L=LCG(m,seed)
FLAG=open("flag.txt",'rb').read()

for i in range(50):
    try:
        choice=json.loads(input("give a message to encrypt\n"))

        if("option" not in choice):
            print("give me an option")
        else:

            if(choice["option"]=="parameters"):
                print(json.dumps({"M":L.m,"a":L.a,"b":L.b}))
                continue

            if(choice["option"]=="get_flag"):
                print(json.dumps({"enc_flag":L.encrypt(FLAG.hex())}))
                continue

            if choice["option"]=="encrypt" and "msgs" in choice:
                msgs=choice["msgs"]
                if(len(msgs)==20):
                    encyrpted_msgs=[]
                    for i in msgs:
                        encyrpted_msgs.append(L.encrypt(i))
                    shuffle(encyrpted_msgs) # swix :)

                    print(json.dumps({"encrypted_msgs":encyrpted_msgs}))
                else:
                    print("give me 64 msgs to encrypt")
                continue

            print("give a valid option")

    except:
        print("dont try something stupid")