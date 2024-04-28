#!/usr/local/bin python3

from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes

def get_key():
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    e = 0x10001
    phi = (p - 1) * (q - 1)
    return (e, n, phi)

def encrypt(m, e, n):
    return pow(m, e, n)

def encrypt_flag(flag, e, n):
    return encrypt(flag, e, n)

def get_flag():
    try:
        with open("/flag") as f:
            FLAG = f.read().strip()
        return FLAG
    except:
        print("[ERROR] - Please contact an Administrator.")

def decrypt_flag(n, e,phi,flag):
    d = pow(e, -1, phi)
    print("hehe adding some impurity so it makes it strong, oh wait this is rsa not steel")
    impurity = encrypt(2, e, n)
    new_flag = impurity * flag
    print(f"Here is the decrypted flag: {pow(new_flag, d, n)}")


def main():
    print("Welcome to the RSA encryption service!")
    e, n , phi = get_key()
    print(f"Here is the public key: (e={e}, n={n})")

    while True:
        print("1. Encrypt a message")
        print("2. Get flag")
        print("3. Decrypt the flag")
        print("4. Exit")
        choice = int(input("Enter your choice: "))


        if choice == 1:
            message = int(input("Enter the message you want to encrypt: "))
            print(f"Here is the encrypted message: {encrypt(message, e, n)}")
        elif choice == 2:
            flag = get_flag().encode()
            print(f"Here is the encrypted flag: {encrypt_flag(bytes_to_long(flag), e, n)}")
        elif choice == 3:
            flag = encrypt_flag(bytes_to_long(get_flag().encode()), e, n)
            decrypt_flag(n,e,phi,flag)
            break
        elif choice == 4:
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()