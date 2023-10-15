from Crypto.Util.number import getPrime, bytes_to_long

p = getPrime(1024)
q = getPrime(512)
n = p * q
e = 65537

FLAG = b"TCP1P{???????????????????????????????????????}"

lock = False
while True:
    print("1. Get new prime")
    print("2. Get leak")
    print("3. Get flag")
    print("4. Exit")
    print("> ", end="")
    try:
        choice = int(input())
    except:
        break
    if choice == 1:
        if lock:
            print("You can't do that anymore!")
            continue
        print("which prime? (p/q)")
        print("> ", end="")
        prime = input()
        if prime == "p":
            p = getPrime(1024)
        elif prime == "q":
            q = getPrime(512)
        else:
            print("What?")
            continue
        n = p * q
        lock = True
    elif choice == 2:
        print("choose leak p ? q (+-*/%)")
        print("> ", end="")
        leak = input()
        if leak == "+":
            print(f"p + q = {pow(p + q, e, n)}") # nuh uh
        elif leak == "-":
            print(f"{p - q = }")
        elif leak == "*":
            print(f"p * q = {pow(p * q, e, n)}") # nuh uh
        elif leak == "/":
            print(f"p // q = {pow(p // q, e, n)}") # nuh uh
        elif leak == "%":
            print(f"{p % q = }")
        else:
            print("What?")
    elif choice == 3:
        print(f"c = {pow(bytes_to_long(FLAG), e, n)}")
        lock = True
    elif choice == 4:
        break
    else:
        print("What?")