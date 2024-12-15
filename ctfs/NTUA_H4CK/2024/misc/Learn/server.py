from secret import FLAG
from Crypto.Cipher import AES
from random import randint,choice,choices
import signal

def timeout_handler(signum, frame):
    print("\nOut of Time 😔")
    exit()

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(20) # Limit to 20s

def rand_str():
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(choices(charset, k=16))

def challenge():
    CNT = 25
    for _ in range(CNT):
        action = choice(['math','aes']) 
        print(f'Challenge: {action}')
        match action:
            case "math":
                a = randint(1,1000)
                b = randint(1,1000)
                operation = choice(['+','-','*','//'])
                inp = input(f"{a} {operation} {b} = ")
                if eval(f"{a} {operation} {b}") != int(inp):
                    return False
                          
            case "aes":
                key = rand_str()
                cipher = AES.new(key.encode(), AES.MODE_ECB)
                s = rand_str()
                s_enc = cipher.encrypt(s.encode())
                print(f'key = {key}')
                print(f'ciphertext = {s_enc.hex()}')
                inp = input("plaintext = ") 
                if inp != s:
                    return False 
                   
        print("Correct, moving on...")  
    return True
    
print("Welcome to the challenge!")
print("Solve 25 challenges to get the flag")
    
if challenge():
    print(FLAG)
else:
    print("Try harder!")


