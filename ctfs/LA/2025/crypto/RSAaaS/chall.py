#!/usr/local/bin/python3

from Crypto.Util.number import isPrime


def RSAaaS():
    try:
        print("Welcome to my RSA as a Service! ")
        print("Pass me two primes and I'll do the rest for you. ")
        print("Let's keep the primes at a 64 bit size, please. ")

        while True:
            p = input("Input p: ")
            q = input("Input q: ")
            try:
                p = int(p)
                q = int(q)
                assert isPrime(p)
                assert isPrime(q)
            except:
                print("Hm, looks like something's wrong with the primes you sent. ")
                print("Please try again. ")
                continue

            try:
                assert p != q
            except:
                print("You should probably make your primes different. ")
                continue

            try:
                assert (p > 2**63) and (p < 2**64)
                assert (q > 2**63) and (q < 2**64)
                break
            except:
                print("Please keep your primes in the requested size range. ")
                print("Please try again. ")
                continue

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        d = pow(e, -1, phi)

        print("Alright! RSA is all set! ")
        while True:
            print("1. Encrypt 2. Decrypt 3. Exit ")
            choice = input("Pick an option: ")

            if choice == "1":
                msg = input("Input a message (as an int): ")
                try:
                    msg = int(msg)
                except:
                    print("Hm, looks like something's wrong with your message. ")
                    continue
                encrypted = pow(msg, e, n)
                print("Here's your ciphertext! ")
                print(encrypted)

            elif choice == "2":
                ct = input("Input a ciphertext (as an int): ")
                try:
                    ct = int(ct)
                except:
                    print("Hm, looks like something's wrong with your message. ")
                    continue
                decrypted = pow(ct, d, n)
                print("Here's your plaintext! ")
                print(decrypted)

            else:
                print("Thanks for using my service! ")
                print("Buh bye! ")
                break

    except Exception:
        print("Oh no! My service! Please don't give us a bad review! ")
        print("Here, have a complementary flag for your troubles. ")
        with open("flag.txt", "r") as f:
            print(f.read())


RSAaaS()
