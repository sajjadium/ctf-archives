from Cryptodome.Util.number import isPrime, bytes_to_long, long_to_bytes
from message import message

def uniqueHash(x):
    steps = 0
    while x != 1:
        steps += 1
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        if steps >= 10000:
            return steps
    return steps


message = bytes_to_long(message)
myHash = uniqueHash(message)

PROOF = 10
print("This is my hash of hash:", uniqueHash(myHash))

prevs = []
steps = 250
while len(prevs) < PROOF:

    x = int(input("Enter your message in hex: "), 16)

    if uniqueHash(x) == myHash and x not in prevs:
        if isPrime(x) == isPrime(message):
            prevs.append(x)
            print("Correct!")
        else:
            print("Well Well, you failed!")

    else:
        print("Incorrect!")

    steps -= 1
    if steps == 0:
        print("Enough fails!")
        quit()

print("Wow! you know my message is:", long_to_bytes(message))