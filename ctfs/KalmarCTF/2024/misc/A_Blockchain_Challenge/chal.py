from Crypto.Util.number import getStrongPrime
from Crypto.Hash import SHA256

e = 65537

# account name to public keys
public_keys = {}
# account name to balances
balances = {}
# account name to secret key, for my own accounts
foundation_accounts_sk = {}

# total value on the blockchain. starts at 10k (9k foundation, 1k you)
total_float = 10000

# probability of block per slot (expected every 5th block)
block_freq = 0.2


def generate_account(name):
    p,q = [getStrongPrime(1024,e=65537) for _ in "pq"]
    d = pow(e,-1,(p-1)*(q-1))
    n = p*q
    pk = n
    sk = d
    return name, pk, sk

def verify_transfer(transfer_request):
    global total_float
    sender, receiver, amount, sig = transfer_request
    pk = public_keys[sender]
    h = SHA256.new()
    h.update(sender.encode() + b':' + receiver.encode() + b':' + str(amount).encode())
    nonce = int(h.hexdigest()*7,16)
    # Some sanity checks
    assert receiver in public_keys, "who are you sending to?"
    assert balances[sender] >=  amount, "illegal transaction detected, aborting"
    assert amount >= 1, "please send enough money to pay for the transaction >.>"
    assert pow(sig,e,pk) == nonce, "invalid signature on transfer request"
    
    balances[sender] -= amount
    balances[receiver] += amount - 1
    total_float -= 1
    print(f'{sender} sent {amount} to {receiver}')
    return 

def verify_generate(generate_request):
    global total_float
    sender, name, sig = generate_request
    # Some sanity checks
    assert name not in public_keys, "that account already exists! get out of here"
    assert ":" not in name, "no delimiters in account names pls"
    assert balances[sender] > 10, "not enough balance to create an account"
    h = SHA256.new()
    h.update(sender.encode() + name.encode())
    nonce =int(h.hexdigest()*7,16)
    assert pow(sig,e,public_keys[sender]) == nonce, "invalid signature on account creation request"
    newname, newpk, newsk = generate_account(name)
    public_keys[newname] = newpk
    balances[newname] = 0
    # Pay the account fee
    balances[sender] -= 10
    total_float -= 10
    print(f'new account created for you!')
    print(f'account name: {newname}')
    print(f'account public key: {newpk}')
    print(f'account private key: {newsk}')

# Check a winning lottery ticket to produce a block
def check_ticket(name, slot):
    global total_float
    # Public Lottery Function, (should probably use a vrf but whatever, no network level attacks here :D)
    # Saw this in ouroborus praos and it looked smart ^^
    winning_prob = 1 - (1 - block_freq)**(balances[name]/total_float)
    h = SHA256.new()
    h.update(b'lottery:::' + str(slot).encode() + b':::' + str(public_keys[name]).encode())
    lottery_roll =int(h.hexdigest(),16)/2**256 
    # did they win the lottery this round?
    if lottery_roll > winning_prob:
        # print("no lottery win, why submit false ticket?")
        return False
    else:
        print(f'account {name} won a block this slot!')
        # Heres your block reward for producing a block!
        balances[name] += 20
        total_float += 20
        print(f'account {name} gained 20 tokens, and now has balance {balances[name]}')
        return True


def get_balances():
    global total_float
    for name in public_keys:
        print(f'{name} has pk {public_keys[name]}')
        print(f'{name} has balance {balances[name]}')
    print(f"total float = {total_float}")


def lottery_foundation_accounts(slot):
    for foundationaccount in foundation_accounts_sk:
        check_ticket(foundationaccount, slot)
    


def verify_win(win_claim):
    name,sig = win_claim
    h = SHA256.new()
    h.update(b'I herebye declare myself victorious!!!!!!!')
    nonce =int(h.hexdigest()*7,16)
    assert pow(sig,e,public_keys[name]) == nonce, "invalid signature"
    assert balances[name] > total_float * 0.51, "you don't have >51 percent of the total_float, go away!"
    print("wow well done! You took over my network!")
    with open("flag.txt", "r") as f:
        print(f.read())
        exit()


if __name__ == "__main__":
    # Set up foundation accounts
    for acc in ["foundation 1", "foundation 2", "foundation 3"]:
         name, pk, sk = generate_account(acc)
         public_keys[name] = pk
         foundation_accounts_sk[name] = sk
         balances[name] = 3000

    # Set up your account with 10% of the stake
    name, pk, sk = generate_account("user")
    public_keys[name] = pk
    balances[name] = 1000

    print(f'Welcome to my blockchain! Its all proof of state and fancy and stuff!')
    print(f'Your name is {name}')
    print(f'your balance is {balances[name]}')
    print(f'your public key is {public_keys[name]}')
    print(f'your private key is {sk}')


    print("lets run a thousand slots!")
    for i in range(1000):
        print(f'Welcome to slot {i}')
        lottery_foundation_accounts(i)

        while True:
            command = input("what would you like to do?")
            if command == "send":
                sender, receiver, amount, sig = input("send request (sender receiver amount sig):").split()
                transfer_request = (sender, receiver, int(amount), int(sig))
                verify_transfer(transfer_request)
            elif command == "create":
                sender, name, sig = input("create request (sender name sig):").split()
                create_request = (sender, name, int(sig))
                verify_generate(create_request)
            elif command == "balance":
                get_balances()
            elif command == "mintblock":
                winner_name = input("block ticket (name):")
                if not check_ticket(winner_name, i):
                    print("why did you submit an invalid ticket?")
                    exit()
                else:
                    break
            elif command == "win":
                name, sig = input("win claim (name sig):").split()
                verify_win((name, int(sig)))
            elif command == "tick":
                break
        
    print("thank you for using my blockchain :)")
    exit()










