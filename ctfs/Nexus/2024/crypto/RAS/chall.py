from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from string import ascii_letters, digits
from random import choice

wisdom = "".join(choice(ascii_letters + digits) for _ in range(16))
passion = getPrime(128)
ambition = getPrime(128)
desire = passion * ambition
willpower = 65537
fate = inverse(willpower, (passion - 1) * (ambition - 1))

insight = pow(bytes_to_long(wisdom.encode()), willpower, desire)

print(f"{insight = }")
print(f"{fate = }")


print("Virtue:")
virtue = input("> ").strip()

if virtue == wisdom:
    print("Victory!!")
    with open("/challenge/flag.txt") as f:
        print(f.read())
else:
    print("Defeat!")