from Crypto.Util.number import getPrime, bytes_to_long

FLAG = b"COMPFEST15{REDACTED}".ljust(256, b"\x00")

class RSA:
    def __init__(self):
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.n = self.p * self.q
        # you can choose your own public exponent
        # self.e = 65537

    def encrypt(self, m, e):
        return pow(m, e, self.n)

    def decrypt(self, c, d):
        return pow(c, d, self.n)


def main():
    print("Welcome to RSA challenge!")
    print("In this challenge you can choose your own public exponent")

    rsa = RSA()
    m = bytes_to_long(FLAG)
    count = 0
    while count < 3:
        print("What do you want to do?")
        print("1. Get encrypted flag")
        print("2. Exit")

        option = input(">> ")
        if option == "1":
            e = int(input("Enter your public exponent (e cannot be 1 and even): "))
            if e == 1 or e % 2 == 0:
                print("loh gak bahaya tah")
                continue
            c = rsa.encrypt(m, e)
            print(f"Here is your encrypted flag: {c}")
            count += 1
        elif option == "2":
            print("Bye!")
            exit()
        else:
            print("Invalid option")
            continue
    
    print("You have reached maximum number of public exponent")

if __name__ == "__main__":
    main()
