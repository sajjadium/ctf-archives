import sys
from rich.progress import track
import random
SALT_RANGE = (150000,250000)
Prev_Mod = 426900
CHUNK_SIZE=4

FLAG = open("FLAG").readline().strip()

def keyedAck(key):
    def ack(m,n):
        if m == 0:
            return n+key
        if n == 0:
            return ack(m-1,1)
        return ack(m-1,ack(m,n-1))
    return ack

def split_flag(flag):
    flag = flag.encode()
    flag = [flag[i:i+CHUNK_SIZE] for i in range(0,len(flag),CHUNK_SIZE)]
    print(flag)
    return [int(i.hex(),16) for i in flag]
def chain(keys):
    out = []
    salts = []
    prev = 0 
    for c_k in track(keys):
        salt = (2,random.randint(*SALT_RANGE)+prev)
        ch = keyedAck(c_k)(*salt)       
        prev = ch % Prev_Mod
        out.append(ch)
        salts.append(salt[1])
    return out,salts

if __name__ == "__main__":
    sf=split_flag(FLAG)
    f= open(f"out{sys.argv[1]}.txt","w")
    f.write(str(chain(sf)))
    f.close()
