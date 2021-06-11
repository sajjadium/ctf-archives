from pwn import remote #pip install pwntools
from hashlib import sha256

def solvepow(p, n):
    s = p.recvline()
    starting = s.split(b'with ')[1][:10].decode()
    s1 = s.split(b'in ')[-1][:n]
    i = 0
    print("Solving PoW...")
    while True:
        if sha256((starting+str(i)).encode('ascii')).hexdigest()[-n:] == s1.decode():
            print("Solved!")
            p.sendline(starting + str(i))
            break
        i += 1

def exploit(p):
    p.interactive()

if __name__ == '__main__':
    p = remote('challs.m0lecon.it', 1337)
    solvepow(p, n = 5)
    exploit(p)
