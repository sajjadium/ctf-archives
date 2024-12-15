from pwn import *
from json import loads,dumps
from hashlib import sha256
context.encoding='ascii'
t = remote('localhost',1337)

def get_belt(seed:int, n:int) -> list[int]:   
    random.seed(seed)
    return [random.randint(1,n**2) for _ in range(n)]

def solve(belt: list[int],k:int) -> list[int]:
    return range(len(belt)) # Replace this with your solution

def main():
    # 3 easy belts, and 5 hard belts
    for _ in range(3 + 5):
        data = loads(t.recvline().decode())
        belt = get_belt(data['seed'],data['n'])
        
        sol  = solve(belt,data['k'])
        
        t.sendline(dumps({'sol_hash':sha256(str(sol).encode()).hexdigest()}))
        
        res = loads(t.recvline().decode())
        
        if res['msg'] != 'Good job! 🎉🎉🎉': # Something went wrong
            print(res)
            exit()
    # GGs
    res = loads(t.recvline().decode())
    print(res['msg'])
    print(res['prize'])
    
    
main()


    


