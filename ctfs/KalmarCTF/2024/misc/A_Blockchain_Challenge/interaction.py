from pwn import *
from Crypto.Hash import SHA256

# my accounts
public_keys = {}
private_keys = {}
balances = {}

# Takes sender name and requested new account name, produces an account on chain.
def account_generate(rem, sender, name):
    assert balances[sender] >= 10
    rem.recvuntil(b'what would you like to do?')
    rem.sendline("create")
    rem.recvuntil(b'create request (sender name sig):')
    h = SHA256.new()
    h.update(sender.encode() + name.encode())
    nonce =int(h.hexdigest()*7,16)
    pk = public_keys[sender]
    sk = private_keys[sender]
    sig = pow(nonce,sk,pk)
    payload = " ".join([sender, name, str(sig)])
    rem.sendline(payload)
    rem.recvuntil("new account created for you!")
    rem.recvuntil("account name: ")
    newname = rem.readline().strip().decode()
    rem.recvuntil("account public key: ")
    newpk = int(rem.readline().strip().decode())
    rem.recvuntil("account private key: ")
    newsk = int(rem.readline().strip().decode())
    public_keys[newname] = newpk
    private_keys[newname] = newsk
    balances[newname] = 0
    balances[sender] -= 10
    return

def transfer(rem, sender, receiver, amount):
    assert balances[sender] >= amount
    rem.recvuntil(b'what would you like to do?')
    rem.sendline("send")
    rem.recvuntil(b'send request (sender receiver amount sig):')
    h = SHA256.new()
    h.update(sender.encode() + b':' + receiver.encode() + b':' + str(amount).encode())
    nonce = int(h.hexdigest()*7,16)
    sig = pow(nonce,private_keys[sender], public_keys[sender])
    payload = " ".join([sender, receiver, str(amount), str(sig)])
    rem.sendline(payload)
    print("waiting for confirmation of send")
    rem.recvuntil(f'{sender} sent {amount} to {receiver}'.encode())
    print("sending success!")
    balances[sender] -= amount
    balances[receiver] += amount - 1
    return


def mintblock(rem, name):
    rem.recvuntil(b'what would you like to do?')
    rem.sendline("mintblock")
    rem.recvuntil(b'block ticket (name):')
    rem.sendline(name)
    balances[name] += 20
    return

def balance(rem):
    rem.recvuntil(b'what would you like to do?')
    rem.sendline("balance")
    data = rem.recvuntil(b'total float').decode()
    data += rem.readline().decode()
    print(data)
    return


def tick(rem):
    rem.recvuntil(b"what would you like to do?")
    rem.sendline("tick")
    return



# with remote(ip, port, level="debug") as rem:
with process(["python3 chal.py"], shell=True, level="debug") as rem:
    rem.recvuntil(b'Your name is ')
    yourname = rem.readline().decode().strip()
    rem.recvuntil(b'your balance is ')
    yourbalance = int(rem.readline().decode().strip())
    rem.recvuntil(b'your public key is ')
    yourpk = int(rem.readline().decode().strip())
    rem.recvuntil(b'your private key is ')
    yoursk = int(rem.readline().decode().strip())
    public_keys[yourname] = yourpk
    private_keys[yourname] = yoursk
    balances[yourname] = yourbalance
    balance(rem)

    account_generate(rem, "user", "account1")
    account_generate(rem, "user", "account2")
    account_generate(rem, "user", "account3")
    balance(rem)

    for i in range(100):
        tick(rem)
    balance(rem)