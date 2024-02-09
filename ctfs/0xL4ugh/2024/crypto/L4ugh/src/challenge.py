from Crypto.Util.number import *
from utils import * 

Flag = '0xL4ugh{Fak3_Fl@g}'
key = os.urandom(16)
x = random.randint(2**10, 2**20)
seed = "It's (666) the work of the devil..."
print(seed)
d = evilRSA(seed)
d_evil = d >> (int(seed[6:9])//2)
d_good = d %  pow(2,int(seed[6:9])//2)
z='''1.d_evil
2.d_good
3.pass d to get to sec part
Ex : {"option":"1"}
d=d_evil+d_good
'''
print('all input data is in json')
print(z)

w='''1.get your token
2.sign in'''
while True:
    test = json.loads(input('option:\t'))
    if test['option'] == "1": 
        Ns,es = RsaGen(d_evil)
        print(f'Ns={Ns}')
        print(f'es={es}')

    if test['option'] == "2":
        res = getrand(d_good)
        print(f'RAND = {res}')

    if test['option'] == "3":
    # check = int(input('Enter the secret key to access admin privileges:\t'))
        if int(test['d']) != d: 
            print("you need to provide d to continue")
            exit()
        elif int(test['d']) == d:
        
            z = json.loads(input(w))
            if z['option'] == '1':
                user = z['user']
                
                data = {"id": x, "isadmin": False, "username": user}
                print(data)
                try:
                    pt = json.dumps(data)
                    ct = encrypt(pt)
                    print(ct)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                x += x
            elif z['option'] == '2':
                token = z['token']
                dec = decrypt(token)
                if dec is not None:
                    print("Decrypted plaintext:", dec)
                else:
                    print("Decryption failed. cant decrypt :",dec) 
                    continue    
                flag(dec)
            


main()