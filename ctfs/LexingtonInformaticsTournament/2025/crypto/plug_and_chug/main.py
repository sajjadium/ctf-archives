from Crypto.Util.number import bytes_to_long, getPrime

n = getPrime(1024)
a = getPrime(1024)
tries = 0

def guess():
    global n
    ans = int(input("What is n? "))
    if ans == n:
        with open("flag.txt", "r") as f:
        print(f"flag: {f.read()}")
    else:
        print("Wrong")
    exit(0)

while tries < 10:
    inp = input("Gimme a number (or type 'guess' to guess): ")
    if inp == "guess":
        guess()
    else:
        x = int(inp)
        if x**2 < 996491788296388609:
            print("Too small")
            continue
        print(pow(a, x, n))
        tries += 1

print("You have used your ten guesses.")
guess()
