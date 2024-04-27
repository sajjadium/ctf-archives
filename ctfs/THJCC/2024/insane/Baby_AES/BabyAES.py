from Crypto.Cipher import AES
import os
import hmac
flag=b'THJCC{FAKE_FLAG}'
key=os.urandom(16)
IV=os.urandom(16)
ecb = AES.new(key, AES.MODE_ECB)
cbc = AES.new(key, AES.MODE_CBC, IV)
passphrase=b'eating_whale...'

def pad(data):
    p = (16 - len(data) % 16) % 16
    return data + bytes([p]) * p

def chk_pad(data):
    if len(data)==16:
        print("Padding Correct")
    elif not all([x == data[-1] for x in data[-data[-1]:]]):
        print("Padding Error")
    else:
        print("Padding Correct")

def sign(x):
    x=pad(x)
    return hmac.new(key, x, 'sha256').hexdigest()

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def MBC(x):
    x=pad(x)
    iv=IV
    final=b''
    for i in range(0, len(x), 16):
        cur=ecb.encrypt(x[i:i+16])
        final+=xor(iv, cur)
        iv=x[i:i+16]
    return final

print("Welcome to my MBC server")
print("It has more security than ECB I think...")
print("Login first, your message should all be hex encoded!")
isadmin=False
while isadmin==False:
    print("We have two functions:")
    print("1.Verify your identity:")
    print("2.Sign a message")
    option=int(input("Option(1/2):"))
    if option!=1 and option !=2:
        print("Error, your choise should be 1 or 2")
    elif option==1:
        x=input("Your signed key(hex encoded):")
        if sign(passphrase)==x:
            print("Verified!!!")
            isadmin=True
        else:
            print("Failed")
    else:
        x=input("Sign a message(hex encoded):")
        if bytes.fromhex(x)==passphrase:
            print("Bad Hacker :(")
        else:
            print(sign(bytes.fromhex(x)))

print("You have two options")
print("This is the encrypted flag(CBC MODE): ") # I know that CBC mode is mush more safer than my MBC mode.
print(cbc.encrypt(pad(flag)).hex())
cbc = AES.new(key, AES.MODE_CBC, IV)
while True:
    print("Option 1: MBC MODE Encrypter")
    print("Option 2: CBC MODE Pad Checker")
    option=int(input("Your option(1/2):"))
    if option == 1:
        x=input("Encrypt a message(hex encoded):")
        print(MBC(bytes.fromhex(x)).hex())
    elif option == 2:
        x=input("Check a padding(hex encoded):")
        chk_pad(cbc.decrypt(pad(bytes.fromhex(x))))
    else:
        print("Invalid method...")