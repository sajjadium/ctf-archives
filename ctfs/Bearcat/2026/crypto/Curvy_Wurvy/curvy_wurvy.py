from random import randint
from ecpy.curves import Curve, Point
from secret import FLAG, MASTER_KEY, FLAG_UID

E = Curve.get_curve('Ed25519')
p = E._domain['order']

def KDF(uid):
    user_key = MASTER_KEY*uid % p
    return user_key

def sign(y, key):
    padding = 0
    while True:
        try:
            x = E.x_recover(y + padding)
            break
        except AssertionError:
            padding += 1
    P = Point(x, y, E)
    signed_point = E.mul_point(key, P)
    return signed_point.y + (padding<<256)

def verify(data, signature, key):
    real_sig = sign(data, key)
    return real_sig == signature

def menu():
    print("What would you like to do?")
    print("1. Get user id")
    print("2. Sign data")
    print("3. Verify signature")
    while True:
        inp = input()
        if inp not in {'1','2','3'}:
            print(f"Invalid choice {inp}")
        else:
            return inp

def main():
    uid_bound = int(pow(p, 1/4))
    print("Welcome to my ECC data signing server!")
    flag_key = KDF(FLAG_UID)
    flag_sig = sign(int.from_bytes(FLAG, 'big'), flag_key)
    
    print(f"Verify the true flag with\nUID: {FLAG_UID}\nSignature: {flag_sig}")
    
    while True:
        choice = menu()
        
        if choice == '1':
            uid = randint(1, uid_bound)
            print(f"Your user id is: {uid}")
            
        elif choice == '2':
            try:
                data = int(input("Enter your data: "))
                uid = int(input("Enter your UID: "))
            except ValueError:
                print("Please enter your data as an integer")
                continue
                
            user_key = KDF(uid)
            sig = sign(data, user_key)
            print(f"Your signature is: {sig}")
            
        elif choice == '3':
            try:
                data = int(input("Enter your data: "))
                uid = int(input("Enter your UID: "))
                sig = int(input("Enter your signature: "))
            except ValueError:
                print("Please enter your data as an integer")
                continue
                
            user_key = KDF(uid)
            if verify(data, sig, user_key):
                print("Verified")
            else:
                print("Verification Failed")
        print()

if __name__ == '__main__':
    main()